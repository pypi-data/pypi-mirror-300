import numpy as np
import h5py
from Snoopy import logger

#---------------------------------------------------------------------#

def write_vtkUnstructuredGrid_vtkhdf(ugrid, filename, mode="w"):
    """Write to HDF vtk format

    Parameters
    ----------
    ugrid : vtk.vtkUnstructuredGrid
        Input data in format vtk.vtkUnstructuredGrid 
    filename : str
        Filename.
    """
    import vtk
    from vtk.util.numpy_support import vtk_to_numpy
    
    if not isinstance(ugrid, vtk.vtkUnstructuredGrid):
        raise TypeError(f"Expect in put as vtkUnstructuredGrid, {type(ugrid)} received!")

    logger.debug(f"Going to write vtkUnstructeredGrid to : {filename}")

    with  h5py.File( filename , mode=mode) as nf : 
        dset = nf.create_group( "VTKHDF" )
        
        dset.attrs.create("Type", np.bytes_("UnstructuredGrid"))
        dset.attrs["Version"] = [1, 0]

        cells = ugrid.GetCells()
        
        dset.create_dataset("NumberOfConnectivityIds", 
                            data  = np.asarray([cells.GetNumberOfConnectivityIds()]), 
                            dtype = np.int64,
                            compression="gzip", compression_opts = 9, shuffle = True)
        
        
        dset.create_dataset("NumberOfPoints", 
                            data  = np.asarray([ugrid.GetNumberOfPoints()]), 
                            dtype = np.int64,
                            compression="gzip", compression_opts = 9, shuffle = True)
        
        dset.create_dataset("NumberOfCells", 
                            data  = np.asarray([cells.GetNumberOfCells()]), 
                            dtype = np.int64, 
                            compression="gzip", compression_opts = 9, shuffle = True)
        
        points = vtk_to_numpy(ugrid.GetPoints().GetData())
        dset.create_dataset("Points", data  = points, chunks =  points.shape,
        compression="gzip", compression_opts = 9, shuffle = True)
        
        connectivity = vtk_to_numpy(cells.GetConnectivityArray())
        dset.create_dataset("Connectivity", data  = connectivity, chunks =  connectivity.shape, 
        compression="gzip", compression_opts = 9, shuffle = True)
        
        offsets = vtk_to_numpy(cells.GetOffsetsArray())
        dset.create_dataset("Offsets", data  =  offsets,chunks =   offsets.shape,
        compression="gzip", compression_opts = 9, shuffle = True)
        
        celltypes = vtk_to_numpy(ugrid.GetCellTypesArray())
        dset.create_dataset("Types",   data  = celltypes ,  chunks =   celltypes.shape,
        compression="gzip", compression_opts = 9, shuffle = True)
        
        all_attribute_types = ["PointData", "CellData", "FieldData"]
        
        for attribute_type_enum,attribute_type_name in enumerate(all_attribute_types):
            field_data = ugrid.GetAttributesAsFieldData(attribute_type_enum)
            nb_array =  field_data.GetNumberOfArrays() 
            if nb_array > 0:

                field_data_group = dset.create_group(attribute_type_name)
                # only for POINT and CELL attributes
                if attribute_type_enum < 2:
                    for i in range(nb_array):
                        array = field_data.GetArray(i)
                        if array:
                            anp = vtk_to_numpy(array)
                            field_data_group.create_dataset(array.GetName(), data = anp, chunks = anp.shape, 
                            compression="gzip", compression_opts = 9, shuffle = True)
                            
                    #for field_type in ["Scalars", "Vectors", "Normals", "Tensors", "TCoords"]:
                    #    array = getattr(field_data, "Get{}".format(field_type))()
                    #    print("Get:", field_type, array)
                    #    if array:
                    #        field_data_group.attrs.create(field_type, np.string_(array.GetName()))
            

            # FIELD attribute
            if attribute_type_enum == 2:
                for i in range(nb_array):
                    array = field_data.GetArray(i)
                    if not array:
                        array = field_data.GetAbstractArray(i)
                        if array.GetClassName() == "vtkStringArray":
                            dtype = h5py.special_dtype(vlen=bytes)
                            dset = field_data_group.create_dataset(
                                array.GetName(),
                                (array.GetNumberOfValues(),), dtype, 
                                compression="gzip", compression_opts = 9, shuffle = True)
                            
                            for index in range(array.GetNumberOfValues()):
                                dset[index] = array.GetValue(index)
                        else:
                            # don't know how to handle this yet. Just skip it.
                            print("Error: Don't know how to write "
                                  "an array of type {}".format(
                                      array.GetClassName()))
                    else:
                        anp = vtk_to_numpy(array)
                        dset = field_data_group.create_dataset(
                            array.GetName(), anp.shape, anp.dtype, chunks = anp.shape, 
                            compression="gzip", compression_opts = 9, shuffle = True)
                        dset[0:] = anp
