# EMRinger outputs positions for pymol
# EMRinger workflow.
# Reference:
# Lang PT, Ng HL, Fraser JS, Corn JE, Echols N, Sales M, Holton JM, Alber T.
# Automated electron-density sampling reveals widespread conformational
# polymorphism in proteins. Protein Sci. 2010 Jul;19(7):1420-31. PubMed PMID:
# 20499387
# 
# Barad BA, Echols N, Wang RYR, Cheng YC, DiMaio F, Adams PD,\n"+
# Fraser JS. Side-chain-directed model and map validation for 3D \n"+
# Electron Cryomicroscopy. Manuscript in preparation.\n"+

import libtbx.phil
import numpy
from libtbx import easy_pickle
from libtbx import easy_mp
from libtbx.str_utils import make_header
from libtbx.utils import Sorry, Usage
from libtbx import adopt_init_args, Auto
from cStringIO import StringIO
import time
import os
import sys
import sqlite3

master_phil = libtbx.phil.parse("""
pdb_file = None
  .type = path
cif_file = None
  .type = path
  .multiple = True
map_coeffs = None
  .type = path
map_label = None
  .type = str
map_file = None
  .type = path
sampling_method = linear *spline direct
  .type = choice(multi=False)
sampling_angle = 1
  .type = int
grid_spacing = 1./5
  .type = float
scaling = *sigma volume
  .type = choice(multi=False)
skip_alt_confs = True
  .type = bool
nproc = 1
  .type = int
show_gui = False
  .type = bool
output_base = None
  .type = str
""")

class ringer_chi (object) :
  def __init__ (self, id, angle_current, densities, sampling) :
    adopt_init_args(self, locals())
    if (angle_current < 0) :
      self.angle_current = 360 + angle_current
    self.peakchi, self.peakrho = self.find_peaks(densities)
    self.deviation = self.deviate(self.peakchi)
    self.meanrho = numpy.mean(densities)
    # Add a tiny number to avoid dividing by 0 (which shouldn't happen anyway)
    self.relrho = self.peakrho/(self.meanrho+.000000000000000001)

  def format_csv (self) :
    return "chi%d,%.1f,%s" % (self.id, self.angle_current, ",".join(
      [ "%.3f" % x for x in self.densities ]))

  def find_peaks (self, densities) :
    for i, j in enumerate(densities):
      if j == max(densities):
        i = i * 5
        return i, j
    # This should never happen, but just in case, dump this in 
    # place of throwing an error.
    return 0,0

  def deviate(self, chi):
    return min(abs(chi-i) for i in [60, 180, 300])



class ringer_residue (object) :
  def __init__ (self, resname, chain_id, resid, altloc, n_chi) :
    adopt_init_args(self, locals())
    self._angles = {}

  def format (self) :
    if (self.altloc == "") :
      return "%s%2s%s" % (self.resname, self.chain_id, self.resid)
    else :
      return "%s%2s%s (conformer %s)" % (self.resname, self.chain_id,
        self.resid, self.altloc)

  def format_csv (self) :
    if (self.altloc == "") :
      prefix = "%s%2s%s," % (self.resname, self.chain_id, self.resid)
    else :
      prefix = "%s%2s%s %s," % (self.resname, self.chain_id, self.resid,
        self.altloc)
    lines = []
    for i in range(1, self.n_chi+1) :
      chi = self.get_angle(i)
      if (chi is not None) :
        lines.append(prefix + chi.format_csv())
    return "\n".join(lines)

  def add_angle (self, **kwds) :
    chi = ringer_chi(**kwds)
    self._angles[chi.id] = chi

  def get_angle (self, id) :
    return self._angles.get(id, None)

def sample_angle (
    i_seqs,
    sites_cart,
    map_coeffs,
    real_map,
    sigma,
    angle_start,
    params,
    unit_cell=None) :
  frac_matrix = None
  if (unit_cell is None) :
    assert (map_coeffs is not None)
    unit_cell = map_coeffs.unit_cell()
  frac_matrix = unit_cell.fractionalization_matrix()
  assert (params.sampling_method != "direct") or (map_coeffs is not None)
  from cctbx import maptbx
  from scitbx.matrix import rotate_point_around_axis
  point = rotate_point_around_axis(
    axis_point_1=sites_cart[1],
    axis_point_2=sites_cart[2],
    point=sites_cart[3],
    angle=-angle_start,
    deg=True)
  # TODO: present option to have point (sites_cart[3]) be generated based on idealized geometry.
  n_degrees = 0
  densities = []
  while (n_degrees < 360) :
    point = rotate_point_around_axis(
      axis_point_1=sites_cart[1],
      axis_point_2=sites_cart[2],
      point=point,
      angle=params.sampling_angle,
      deg=True)
    point_frac = unit_cell.fractionalize(site_cart=point)
    if (params.sampling_method == "spline") and (map_coeffs is not None) :
      rho = real_map.tricubic_interpolation(point_frac)
    elif (params.sampling_method == "linear") or (map_coeffs is None) :
      if (map_coeffs is None) :
        rho = maptbx.non_crystallographic_eight_point_interpolation(
          map=real_map,
          gridding_matrix=frac_matrix,
          site_cart=point)
          #allow_out_of_bounds=True)
      else :
        rho = real_map.eight_point_interpolation(point_frac)
    else :
      rho = map_coeffs.direct_summation_at_point(
        site_frac=point_frac,
        sigma=sigma).real
    densities.append(point)
    n_degrees += params.sampling_angle
  #print densities
  return densities

class iterate_over_residues (object) :
  def __init__ (self,
                pdb_hierarchy,
                params,
                map_coeffs=None,
                ccp4_map=None,
                unit_cell=None,
                log=None) :
    if (log is None) : log = sys.stdout
    adopt_init_args(self, locals())
    models = pdb_hierarchy.models()
    if (len(models) > 1) :
      raise Sorry("Multi-model PDB files not supported.")
    self.sigma = self.real_map = None
    if (map_coeffs is not None) :
      self.unit_cell = map_coeffs.unit_cell()
      if (params.sampling_method == "direct") :
        self.map_coeffs = self.map_coeffs.expand_to_p1()
        if (not map_coeffs.anomalous_flag()) :
          self.map_coeffs = self.map_coeffs.generate_bijvoet_mates()
      if (params.sampling_method != "direct") or (params.scaling == "sigma") :
        fft_map = self.map_coeffs.fft_map(resolution_factor=params.grid_spacing)
        if (params.scaling == "sigma") :
          self.sigma = fft_map.statistics().sigma()
          fft_map.apply_sigma_scaling()
        else :
          fft_map.apply_volume_scaling()
        self.real_map = fft_map.real_map_unpadded()
    else :
      assert (ccp4_map is not None)
      print >> self.log, "CCP4 map statistics:"
      ccp4_map.show_summary(out=self.log, prefix="  ")
      self.real_map = ccp4_map.data.as_double()
      # XXX assume that the map is already scaled properly (in the original
      # unit cell)
      self.sigma = 1 #ccp4_map.statistics().sigma()
      # XXX the unit cell that we need for the non-crystallographic
      # interpolation is not what comes out of the map - it's the
      from cctbx import uctbx
      unit_cell = ccp4_map.unit_cell()
      a = unit_cell.parameters()[0] / ccp4_map.unit_cell_grid[0]
      b = unit_cell.parameters()[1] / ccp4_map.unit_cell_grid[1]
      c = unit_cell.parameters()[2] / ccp4_map.unit_cell_grid[2]
      alpha,beta,gamma = unit_cell.parameters()[3:6]
      self.unit_cell = uctbx.unit_cell((a,b,c,alpha,beta,gamma))
      # FIXME should use this instead (once it's available)
      #self.unit_cell = ccp4_map.grid_unit_cell()
    results = []
    from mmtbx.rotamer import sidechain_angles
    self.angle_lookup = sidechain_angles.SidechainAngles(False)
    self.sites_cart = pdb_hierarchy.atoms().extract_xyz()
    self.residue_groups = []
    for chain in models[0].chains() :
      self.residue_groups.extend(chain.residue_groups())
    if (params.nproc in [None,Auto]) or (params.nproc > 1) :
      # this will be a list of lists
      results_ = easy_mp.pool_map(
        processes=params.nproc,
        fixed_func=self.sample_density,
        args=range(len(self.residue_groups)))
      # now flatten it out
      self.results = []
      for result_list in results_ : self.results.extend(result_list)
    else :
      self.results = []
      for i_res in range(len(self.residue_groups)) :
        self.results.extend(self.sample_density(i_res, verbose=True))

  def sample_density (self, i_res, verbose=False) :
    import iotbx.pdb
    get_class = iotbx.pdb.common_residue_names_get_class
    residue_group = self.residue_groups[i_res]
    conformers = residue_group.conformers()
    results = []
    for i_conf, conformer in enumerate(residue_group.conformers()) :
      if (i_conf > 0) and (self.params.skip_alt_confs) :
        continue
      residue = conformer.only_residue()
      if (get_class(residue.resname) == "common_amino_acid") :
        n_chi = int(self.angle_lookup.chisPerAA.get(residue.resname.lower(),0))
        if (n_chi == 0) : continue
        res_out = ringer_residue(
          #residue_id_str=residue.id_str(),
          resname=residue.resname,
          chain_id=residue_group.parent().id,
          resid=residue.resid(),
          altloc=conformer.altloc,
          n_chi=n_chi)
        if (verbose) :
          print >> self.log, "  %s:" % residue.id_str()
        for i in range(1, n_chi+1) :
          try :
            atoms = self.angle_lookup.extract_chi_atoms("chi%d" % i, residue)
          except AttributeError :
            print >> "AttributeError"
            pass
          else :
            # Skip a chi angle if it doesn't work.
            try:
              i_seqs = [ atom.i_seq for atom in atoms ]
              sites_chi = [ self.sites_cart[i_seq] for i_seq in i_seqs ]
              from cctbx.geometry_restraints import dihedral
              chi = dihedral(
                sites=sites_chi,
                angle_ideal=0,
                weight=0)
              if (verbose) :
                print >> self.log, "    chi%d = %.1f" % (i, chi.angle_model)
              densities = sample_angle(
                i_seqs=i_seqs,
                sites_cart=sites_chi,
                map_coeffs=self.map_coeffs,
                real_map=self.real_map,
                unit_cell=self.unit_cell,
                angle_start=chi.angle_model,
                sigma=self.sigma,
                params=self.params)
              if (verbose) : pass
              res_out.add_angle(
                id=i,
                angle_current=chi.angle_model,
                densities=densities,
                sampling=self.params.sampling_angle)
            # This is a pretty bad way to deal with it but I don't want to stop 
            # the whole program because of a problem such as a missing atom...
            except: print "Problem with ringing"
        results.append(res_out)
    return results

def run (args, out=None, verbose=True) :
  t0 = time.time()
  if (out is None) : out = sys.stdout
  if (len(args) == 0) :
    phil_out = StringIO()
    master_phil.show(out=phil_out, prefix="    ")
    raise Usage("ringer.py [model.pdb] [map.mtz] [cif_file ...] [options]\n"+
      "  Reference:\n"+
      "    Lang PT, Ng HL, Fraser JS, Corn JE, Echols N, Sales M, Holton\n"+
      "    JM, Alber T.  Automated electron-density sampling reveals\n"+
      "    widespread conformational polymorphism in proteins. Protein Sci.\n"+
      "    2010 Jul;19(7):1420-31. PubMed PMID: 20499387\n"+
      "  Full parameters:\n%s" % phil_out.getvalue())
  from iotbx import file_reader
  import iotbx.phil
  cmdline = iotbx.phil.process_command_line_with_files(
    args=args,
    master_phil=master_phil,
    pdb_file_def="pdb_file",
    reflection_file_def="map_coeffs",
    map_file_def="map_file",
    cif_file_def="cif_file")
  params = cmdline.work.extract()
  validate_params(params)
  pdb_in = file_reader.any_file(params.pdb_file, force_type="pdb")
  pdb_in.check_file_type("pdb")
  hierarchy = pdb_in.file_object.construct_hierarchy()
  hierarchy.atoms().reset_i_seq()
  map_coeffs = ccp4_map = None
  if (params.map_coeffs is not None) :
    mtz_in = file_reader.any_file(params.map_coeffs, force_type="hkl")
    mtz_in.check_file_type("hkl")
    best_guess = None
    best_labels = []
    all_labels = []
    for array in mtz_in.file_server.miller_arrays :
      if (array.info().label_string() == params.map_label) :
        map_coeffs = array
        break
      elif (params.map_label is None) :
        if (array.is_complex_array()) :
          labels = array.info().label_string()
          all_labels.append(labels)
          if (labels.startswith("2FOFCWT") or labels.startswith("2mFoDFc") or
              labels.startswith("FWT")) :
            best_guess = array
            best_labels.append(labels)
    if (map_coeffs is None) :
      if (len(all_labels) == 0) :
        raise Sorry("No valid (pre-weighted) map coefficients found in file.")
      elif (best_guess is None) :
        raise Sorry("Couldn't automatically determine appropriate map labels. "+
          "Choices:\n  %s" % "  \n".join(all_labels))
      elif (len(best_labels) > 1) :
        raise Sorry("Multiple appropriate map coefficients found in file. "+
          "Choices:\n  %s" % "\n  ".join(best_labels))
      map_coeffs = best_guess
      print >> out, "  Guessing %s for input map coefficients" % best_labels[0]
  else :
    ccp4_map_in = file_reader.any_file(params.map_file, force_type="ccp4_map")
    ccp4_map_in.check_file_type("ccp4_map")
    ccp4_map = ccp4_map_in.file_object
  make_header("Iterating over residues", out=out)
  t1 = time.time()
  results = iterate_over_residues(
    pdb_hierarchy=hierarchy,
    map_coeffs=map_coeffs,
    ccp4_map=ccp4_map,
    params=params,
    log=out).results
  t2 = time.time()
  if (verbose) :
    print >> out, "Time excluding I/O: %8.1fs" % (t2 - t1)
    print >> out, "Overall runtime:    %8.1fs" % (t2 - t0)
  if (params.output_base is None) :
    pdb_base = os.path.basename(params.pdb_file)
    params.output_base = os.path.splitext(pdb_base)[0] + "_ringer_rings"
  easy_pickle.dump("%s.pkl" % params.output_base, results)
  print >> out, "Wrote %s.pkl" % params.output_base
  # csv = "\n".join([ r.format_csv() for r in results ])
  # open("%s.csv" % params.output_base, "w").write(csv)
  # print >> out, "Wrote %s.csv" % params.output_base
  print >> out, "\nReference:"
  print >> out, """\
  Lang PT, Ng HL, Fraser JS, Corn JE, Echols N, Sales M, Holton JM, Alber T.
  Automated electron-density sampling reveals widespread conformational
  polymorphism in proteins. Protein Sci. 2010 Jul;19(7):1420-31. PubMed PMID:
  20499387"""
  if (params.show_gui) :
    run_app(results)
  else :
    return results

def validate_params (params) :
  if (params.pdb_file is None) :
    raise Sorry("No PDB file supplied (parameter: pdb_file)")
  if (params.map_coeffs is None) and (params.map_file is None) :
    raise Sorry("No map coefficients supplied (parameter: map_coeffs)")
  return True

########################################################################
# GUI
from wxtbx import plots
import wx

def run_app (results) :
  app = wx.App(0)
  frame = RingerFrame(None, -1, "Ringer results")
  frame.show_results(results)
  frame.Show()
  app.MainLoop()

class RingerFrame (plots.plot_frame) :
  def create_plot_panel (self) :
    plot = RingerPlot(self, figure_size=(6,8))
    plot.canvas.Bind(wx.EVT_CHAR, self.OnChar)
    return plot

  def draw_top_panel (self) :
    self.top_panel = wx.Panel(self, style=wx.SUNKEN_BORDER)
    panel_szr = wx.BoxSizer(wx.VERTICAL)
    self.top_panel.SetSizer(panel_szr)
    szr2 = wx.BoxSizer(wx.HORIZONTAL)
    panel_szr.Add(szr2)
    txt1 = wx.StaticText(self.top_panel, -1, "Residue to display:")
    szr2.Add(txt1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
    self.chooser = wx.Choice(self.top_panel, -1, size=(200,-1))
    szr2.Add(self.chooser, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
    self.Bind(wx.EVT_CHOICE, self.OnSelect, self.chooser)
    self.Bind(wx.EVT_CHAR, self.OnChar)
    self.chooser.Bind(wx.EVT_CHAR, self.OnChar)
    return self.top_panel

  def OnSelect (self, event) :
    selection = event.GetEventObject().GetSelection()
    self.plot_panel.show_residue(self.results[selection])

  def show_results (self, results) :
    self.results = results
    choices = [ result.format() for result in results ]
    self.chooser.SetItems(choices)
    self.chooser.SetSelection(0)
    self.plot_panel.show_residue(self.results[0])

  def OnChar (self, event) :
    key = event.GetKeyCode()
    if (len(self.results) == 0) : return
    selection = self.chooser.GetSelection()
    if (key in [wx.WXK_TAB, wx.WXK_RETURN, wx.WXK_SPACE]) :
      if (selection < (len(self.results) - 1)) :
        selection += 1
      elif (len(self.results) > 0) :
        selection = 0
    elif (key in [wx.WXK_DELETE, wx.WXK_BACK]) :
      if (selection > 0) :
        selection -= 1
      else :
        selection = len(results) - 1
    self.chooser.SetSelection(selection)
    self.plot_panel.show_residue(self.results[selection])

class RingerPlot (plots.plot_container) :
  def show_residue (self, residue) :
    if (self.disabled) : return
    self.figure.clear()
    subplots = []
    for i in range(1, residue.n_chi + 1) :
      chi = residue.get_angle(i)
      if (chi is None) : continue
      if (len(subplots) > 0) :
        p = self.figure.add_subplot(4, 1, i, sharex=subplots[0])
      else :
        p = self.figure.add_subplot(4, 1, i)
        p.set_title(residue.format())
      p.set_position([0.15, 0.725 - 0.225*(i-1), 0.8, 0.225])
      x = [ k*chi.sampling for k in range(len(chi.densities)) ]
      p.plot(x, chi.densities, 'r-', linewidth=1)
      p.axvline(chi.angle_current, color='b', linewidth=2, linestyle='--')
      p.axvline(chi.peakchi, color='g', linewidth=2, linestyle = '--')
      p.axhline(0, color=(0.4,0.4,0.4), linestyle='--', linewidth=1)
      p.axhspan(0.3,1,facecolor="green",alpha=0.5)
      p.axhspan(-1,0.3,facecolor="grey",alpha=0.5)
      p.set_xlim(0,360)
      ax = p.get_axes()
      ax.set_ylabel("Rho")
      ax.set_xlabel("Chi%d" % i)
      subplots.append(p)
    for p in subplots[:-1] :
      for label in p.get_axes().get_xticklabels() :
        label.set_visible(False)
    p.text(0,-0.5,'Green = Peak, Blue = Modelled',
        transform=ax.transAxes)
    self.canvas.draw()
    self.canvas.Fit()
    self.Layout()
    self.parent.Refresh()

if (__name__ == "__main__") :
  run(sys.argv[1:])
