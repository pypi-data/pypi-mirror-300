from shadow4.beamline.s4_beamline import S4Beamline

beamline = S4Beamline()

#
#
#
from shadow4.sources.source_geometrical.source_grid_cartesian import SourceGridCartesian

light_source = SourceGridCartesian(name='Grid Source (Cartesian)',
                                   real_space_width=[0.000005, 0.000000, 0.000005],
                                   real_space_center=[0.000000, 0.000000, 0.000000],
                                   real_space_points=[11, 1, 11],
                                   direction_space_width=[0.020000, 0.020000],
                                   direction_space_center=[0.000000, 0.000000],
                                   direction_space_points=[1, 1],
                                   wavelength=1.10013e-10,
                                   polarization_degree=1,
                                   polarization_phase_deg=0,
                                   coherent_beam=1)
beam = light_source.get_beam()

beamline.set_light_source(light_source)

# optical element number XX
from syned.beamline.shape import Ellipse

boundary_shape = Ellipse(a_axis_min=-0.0002, a_axis_max=0.0002, b_axis_min=-0.0002, b_axis_max=0.0002)

from shadow4.beamline.optical_elements.refractors.s4_conic_interface import S4ConicInterface

optical_element = S4ConicInterface(name='Refractive Interface Be', boundary_shape=boundary_shape,
                                   f_r_ind=2,  # source of optical constants:
                                   # (0) cte in both object (O) and image (I) spaces,
                                   # (1) file in O, cte in I, (2) cte in O, file in I, (3) file in O and I
                                   # (4) xraylib in O, cte in I, (5) cte O, xraylib in I, (6) xraylib in O and I
                                   # (7) dabax O, cte in I, (8) cte value in O, dabax in I, (9) dabax in O and I
                                   material_object='', material_image='',
                                   density_object=1, density_image=1,
                                   r_ind_obj=1, r_ind_ima=0.999997,
                                   r_attenuation_obj=0, r_attenuation_ima=0,
                                   file_r_ind_obj='<none>', file_r_ind_ima='/home/srio/Oasys/Be.dat',
                                   dabax=None,
                                   conic_coefficients=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0])
ideal_interface = optical_element
boundary_shape = None
from shadow4.beamline.optical_elements.refractors.s4_numerical_mesh_interface import S4NumericalMeshInterface

optical_element = S4NumericalMeshInterface(name='Undefined',
                                           boundary_shape=boundary_shape,
                                           xx=None, yy=None, zz=None, surface_data_file='/home/srio/Oasys/tmp.hdf5',
                                           f_r_ind=0,  # source of optical constants:
                                           # (0) cte in both object (O) and image (I) spaces,
                                           # (1) file in O, cte in I, (2) cte in O, file in I, (3) file in O and I
                                           # (4) xraylib in O, cte in I, (5) cte O, xraylib in I, (6) xraylib in O and I
                                           # (7) dabax O, cte in I, (8) cte value in O, dabax in I, (9) dabax in O and I
                                           material_object='', material_image='',
                                           density_object=1, density_image=1,
                                           r_ind_obj=1, r_ind_ima=1,
                                           r_attenuation_obj=0, r_attenuation_ima=0,
                                           file_r_ind_obj='', file_r_ind_ima='',
                                           dabax=None,
                                           )
numerical_mesh_interface = optical_element
boundary_shape = None

from shadow4.beamline.optical_elements.refractors.s4_additional_numerical_mesh_interface import \
    S4AdditionalNumericalMeshInterface

optical_element = S4AdditionalNumericalMeshInterface(name='ideal + surface error', ideal_interface=ideal_interface,
                                                     numerical_mesh_interface=numerical_mesh_interface)

from syned.beamline.element_coordinates import ElementCoordinates

coordinates = ElementCoordinates(p=0.52, q=2.6, angle_radial=0, angle_azimuthal=0, angle_radial_out=3.141592654)
movements = None
from shadow4.beamline.optical_elements.refractors.s4_additional_numerical_mesh_interface import \
    S4AdditionalNumericalMeshInterfaceElement

beamline_element = S4AdditionalNumericalMeshInterfaceElement(optical_element=optical_element, coordinates=coordinates,
                                                             movements=movements, input_beam=beam)

beam, mirr = beamline_element.trace_beam()

beamline.append_beamline_element(beamline_element)

# test plot
if True:
    from srxraylib.plot.gol import plot_scatter

    plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)',
                 plot_histograms=0)
    plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')