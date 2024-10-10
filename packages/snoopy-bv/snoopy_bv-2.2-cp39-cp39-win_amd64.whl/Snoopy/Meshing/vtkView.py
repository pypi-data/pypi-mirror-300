"""Contains high-level routines to help the use of VTK
"""

import numpy as np
from Snoopy import logger
from Snoopy.PyplotTools import vtkLookupTable_from_cmap



camera_preset_catalogue = {   "bottom" : { "camPosition": [ 0.0, 0.0, 10.0],
                                 "viewAngle": None,
                                 "targetPosition": [0.0, 0.0, 0.0],
                                 "viewUp": [0, 1, 0],
                                 "fitView": 1.0,  }, 
                 
                    "left" : {  "camPosition": [ 0.0, +10.0, 0.0],
                                "viewAngle": None,
                                "targetPosition": [0.0, 0.0, 0.0],
                                "viewUp": [0, 0, 1],
                                "fitView": 3.,  },

                    "right" : {  "camPosition": [ 0.0, -10.0, 0.0],
                                "viewAngle": None,
                                "targetPosition": [0.0, 0.0, 0.0],
                                "viewUp": [0, 0, 1],
                                "fitView": 1.0,  },
                    
                    "fore_top" : {  "camPosition": [ 3.0, 1.0, 1.0],
                                    "targetPosition": [0.5, 0.5, 0.0],
                                    "viewAngle": 30.,
                                    "viewUp": [0, 0, 1],
                                     "fitView": 1.0,  }, 
                    
                    "fore_bottom" : {  "camPosition": [ 3.0, 1.0, -1.0],
                                    "targetPosition": [0.5, 0.5, 0.0],
                                    "viewAngle": 30.,
                                    "viewUp": [0, 0, 1],
                                     "fitView": 1.0,  },
                    
                    "default" : {   "camPosition": [-10.0, 0.0, 0.0],
                                    "viewAngle": 30,
                                    "scale": 1.0,
                                    "targetPosition": [0.0, 0.0, 0.0],
                                    "viewUp": [0, 0, 1],
                                    "fitView": 1.0,
                                }

                }


class VtkLite():
    """High level layer for handling visualization of single, surface mesh
    """
    def __init__( self, mapper, display_props = {}, camera_preset = "default", camera_kwds = {} , cbar = False):
        """Class handling simple VTK visualisation.

        Parameters
        ----------
        mapper : vtkMapper
            A vtk mapper
        display_props : dict, optional
            Display properties. The default is {}.
        camera_preset : str, optional
            Camera preset. The default is "default".
        camera_kwds : dict, optional
            Change to preset camera setting. The default is {}.
        cbar : bool, optional
            Whether to display a color bar. The default is False.
            
            
        Parameters display_props
        ------------------------
        cell_field : str
            Field used to color the mesh
        point_field : str
            Field used to color the mesh
        color : tuple
            RGB color
            
        Parameters camera_kwds
        ------------------------
        fitView : float or None
            Automatic zoom.
              
            
        Example
        -------
        >>> v = msh.vtkView.VtkLite.FromMesh(m, camera_preset = "left", camera_kwds = { "fitView" : 2.0},  display_props = {"edges" : 1 , "color" : [1.0, 0.0, 0.0]})
        >>> v.to_interactive( size = (800,300) )
        
        """
        import vtk
        self.mapper = mapper
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(mapper)

        self.renderer = vtk.vtkRenderer()
        self.renderer.AddActor(self.actor)
        self.renderer.SetBackground(1, 1, 1)  # White background
        
        # Should be put in "view" routines?
        self.set_properties(display_props)
        self.set_camera(camera_preset, camera_kwds)
        
        if cbar:
            self.renderer.AddActor(addColorBar(self.actor, title= display_props.get("cell_field" , display_props.get("point_field", "" )) ))
        

    def set_properties(self, display_props):
        setDisplayProperties(self.actor, **display_props)

            
    def set_camera(self, camera_preset = "default", camera_kwds = {}):
        camera_ = camera_preset_catalogue[camera_preset]
        camera_.update( **camera_kwds )
        setCamera(self.renderer, **camera_)

        
    @classmethod
    def FromPolydata(cls, polydata, **kwargs):
        import vtk
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData( polydata )
        return cls(mapper , **kwargs)
    
    
    @classmethod
    def FromVtuFile(cls, vtk_file, *args, **kwargs):
        import vtk
        r = vtk.vtkUnstructuredGridReader()
        r.SetFileName(vtk_file)
        r.Update()
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(r.GetOutputPort())
        return cls( mapper , *args, **kwargs )
    
    @classmethod
    def FromMesh(cls, mesh, *args, **kwargs):
        p = mesh.convertToVtk()
        return cls.FromPolydata(p, *args, **kwargs)





    def set_osp_ray(self):
        print("Using ospray")
        import vtk
        osprayPass = vtk.vtkOSPRayPass()

        self.renderer.SetPass(osprayPass)

        osprayNode = vtk.vtkOSPRayRendererNode()
        osprayNode.SetEnableDenoiser(1, self.renderer)

        osprayNode.SetSamplesPerPixel(4,self.renderer)
        osprayNode.SetAmbientSamples(0,self.renderer)
        osprayNode.SetMaxFrames(4, self.renderer)

        osprayNode.SetRendererType("pathtracer", self.renderer);

        osprayNode.SetBackgroundMode(osprayNode.Environment, self.renderer)

        self.renderer.SetEnvironmentUp( -1 , 0. , 0.0)
        self.renderer.SetEnvironmentRight( 0 , -1 , 0)

        self.renderer.SetEnvironmentalBG(0.0, 0.9, 0.0)
        self.renderer.SetEnvironmentalBG2(0.0, 0.9, 0.0)
        self.renderer.GradientEnvironmentalBGOn()

        ml = vtk.vtkOSPRayMaterialLibrary()
        ml.AddMaterial("metal_1", "thinGlass")
        ml.AddShaderVariable("metal_1", "attenuationColor", 3,  [ 0.0, 0.9, 0.0 ])

        osprayNode.SetMaterialLibrary(ml, self.renderer)
        self.actor.GetProperty().SetMaterialName("metal_1")
        self.actor.GetProperty().SetEdgeVisibility(1)


    def add_line(self, start , stop, display_props = {} ):
        """Add a line to the view.

        Parameters
        ----------
        start : TYPE
            DESCRIPTION.
        stop : TYPE
            DESCRIPTION.
        display_props : TYPE, optional
            DESCRIPTION. The default is {}.
        """
        import vtk
        
        ls = vtk.vtkLineSource()
        ls.SetPoint1(*start)
        ls.SetPoint2(*stop)

        m = vtk.vtkDataSetMapper()
        m.SetInputConnection( ls.GetOutputPort() )

        a = vtk.vtkActor()
        a.SetMapper(m)

        setDisplayProperties( a,  **display_props )
        self.renderer.AddActor(a)



    def to_picture(self, output_file , size =  (1650, 1050) ) :
        renderer_to_picture( self.renderer, output_file , size = size )
        
        
    def to_interactive(self, size = (800,600) ):
        import vtk
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.SetSize(*size)
        renderWindow.AddRenderer( self.renderer )
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)
        renderWindowInteractor.SetInteractorStyle( vtk.vtkInteractorStyleTrackballCamera() )
        renderWindow.Render()
        renderWindowInteractor.Start()

    def to_notebook(self, *args, **kwargs):
        return vtk_show( self.renderer, *args, **kwargs )



def writerFromExt(ext):
    """Pick correct vtk writter class based on extension

    Parameters
    ----------
    ext : srt
        File extension of filename, among [.png, .jpg, .bmp, .eps, .tiff]

    Returns
    -------
    writer : vtk.vtkWriter
        Writer class
    """
    import vtk

    ext_ = ext.split(".")[-1]

    if ext_ == "png":
        writer = vtk.vtkPNGWriter
    elif ext_ == "jpg":
        writer = vtk.vtkJPEGWriter
    elif ext_ == "bmp":
        writer = vtk.vtkBMPWriter
    elif ext_ == "eps":
        writer = vtk.vtkPostScriptWriter
    elif ext_ == "tiff":
        writer = vtk.vtkTIFFWriter
    else:
        raise (Exception(f"Picture extension not recognized : {ext:}"))
    return writer




def printCamera(cam):
    str_ = f"""
Position    : {cam.GetPosition():}
Focal point : {cam.GetFocalPoint():}
Parallel    : {cam.GetParallelProjection():}
ParallelScale : {cam.GetParallelScale():}
ViewAngle   : {cam.GetViewAngle():}
"""
    return str_


def setCamera(
    renderer,
    camPosition=None,
    targetPosition=None,
    viewAngle=30.0,
    scale=None,
    fitView = 0.9,
    viewUp=[0, 0, 1],
    reduceFittedDistance=None,
    ):
    """Set camera positon

    Parameters
    ----------
    renderer : vtk.vtkRenderer
        The vtk renderer
    camPosition : tuple, optional
        Camera position coordinates (x,y,z). The default is None.
    targetPosition : tuple, optional
        Camera focus point coordinates (x,y,z). The default is None.
    viewAngle : float, optional
        Angle for perspective view. The default is 30..
    scale : float, optional
        scale. The default is None.
    fitView : bool, optional
        If True, the view is automatically fitted to geometry. The default is True.
    viewUp : tuple, optional
        Camera upward position. The default is [0,0,1].
    reduceFittedDistance : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    None.
    """

    camera = renderer.GetActiveCamera()

    if camPosition is not None:
        camera.SetPosition(camPosition)
    if targetPosition is not None:
        camera.SetFocalPoint(targetPosition)
    camera.SetDistance(1.)
    camera.SetViewUp(viewUp)
    
    if viewAngle is not None:
        camera.SetViewAngle(viewAngle)
        camera.SetParallelProjection(False)

    if fitView or camPosition is None or targetPosition is None:
        renderer.ResetCamera( )
        # renderer.ResetCameraScreenSpace()
        
        if isinstance( fitView, float ) : 
            camera.Zoom(fitView)
            #renderer.ResetCameraScreenSpace( offsetRatio= fitView )

    if viewAngle is None:
        if fitView:
            d = camera.GetDistance()
            a = camera.GetViewAngle()
            camera.SetParallelScale(d * np.tan(0.5 * (a * np.pi / 180)))
            camera.SetParallelProjection(True)
        else:
            camera.SetParallelProjection(True)
            camera.SetParallelScale(scale)

    logger.debug(printCamera(camera))

    return



def setDisplayProperties(
    actor,
    cell_field = None,
    point_field = None,
    cmap="cividis",
    scalarRange = None,
    edges=0,
    opacity=1.0,
    component = None,
    color = [0.5,0.5,0.5],
    update_mapper = False
):
    """Specify field to use to mapper

    Parameters
    ----------
    mapper : vtk.vtkMapper
        The mapper
    scalarField : str
        field to plot
    scalarRange : tuple, None or "auto"
        Color map bounds. if "auto", datarange is used (might not work if several time steps)
    cmap : str or vtk.vtkLookUpTable
        Color map
    update_mapper : bool
        Whether to update the mapper before applying the properties, this is only useful for actual check of field availability.
    """

    mapper = actor.GetMapper()

    if update_mapper:     
        mapper.Update()

    if cell_field or point_field:
        
        if cell_field : 
            data_source = "cell"
            cd = mapper.GetInputAsDataSet().GetCellData()
            available_field = [ cd.GetArrayName(i) for i in range(cd.GetNumberOfArrays()) ]
            if cell_field not in available_field and not update_mapper :
                logger.warning( f"{cell_field:} not available in {available_field:}" )

            mapper.SetScalarModeToUseCellFieldData()
            mapper.SelectColorArray(cell_field)
        else: 
            data_source="point"
            cd = mapper.GetInputAsDataSet().GetPointData()
            available_field = [ cd.GetArrayName(i) for i in range(cd.GetNumberOfArrays()) ]
            if point_field not in available_field and not update_mapper :
                logger.warning( f"{point_field:} not available in {available_field:}" )
            
            mapper.SetScalarModeToUsePointFieldData()
            mapper.SelectColorArray(point_field)
            
        # mapper.SetUseLookupTableScalarRange(0)
        if scalarRange is not None:
            if scalarRange == "auto":
                # FIXME : there is probably a simpler and more general way...
                try:
                    if data_source.lower() == "cell":
                        sr = (
                            mapper.GetInputAsDataSet()
                            .GetCellData()
                            .GetArray(cell_field)
                            .GetValueRange()
                        )
                    if data_source.lower() == "point":
                        sr = (
                            mapper.GetInputAsDataSet()
                            .GetPointData()
                            .GetArray(point_field)
                            .GetValueRange()
                        )
                except Exception:
                    logger.warning(
                        f"{cell_field:} {point_field} not there yet. Cannot set color map range"
                    )
            else:
                sr = scalarRange
                mapper.SetUseLookupTableScalarRange(False)
                mapper.SetScalarRange(*sr)
         
        
        if isinstance(cmap, str):
            lut = vtkLookupTable_from_cmap(cmap)
        else:
            lut = cmap

        mapper.SetLookupTable(lut)

        if component is not None:
            mapper.GetLookupTable().SetVectorComponent(component)
            lut.SetVectorModeToComponent()
        else : 
            lut.SetVectorModeToMagnitude()
    else :
        mapper.SetScalarVisibility(False)
        actor.GetProperty().SetColor( color )
        
    # Properties
    actor.GetProperty().SetEdgeVisibility(edges)
    actor.GetProperty().SetOpacity(opacity)




def addColorBar(actor, title="?", width=0.05, height=0.25):
    """Create color bar actor

    Parameters
    ----------
    actor : vtk.vtkActor
        The actor

    Return
    ------
    vtk.vtkScalarBarActor
       The color bar actor
    """
    import vtk

    # --- Color bar legend
    lut = actor.GetMapper().GetLookupTable()
    scalarBar = vtk.vtkScalarBarActor()
    scalarBar.SetLookupTable(lut)
    scalarBar.SetWidth(width)
    scalarBar.SetHeight(height)
    scalarBar.SetTitle(title)
    scalarBar.GetTitleTextProperty().SetColor(0.0, 0.0, 0.0)
    scalarBar.GetLabelTextProperty().SetColor(0.0, 0.0, 0.0)
    return scalarBar


def renderer_to_picture(renderer, pictureFile, size = (1650, 1050), mag = 1,  large_image = False ):
    """Set camera positon

    Parameters
    ----------
    renderer : vtk.vtkRenderer
        The vtk renderer
    pictureFile : str
        Output picture name
    size : tuple(float)
        Resolution of the output picture, if none, the current/default renderering size is used.
    mag : int
        Magnification factors
    large_image : bool
        If True, uses vtkRenderLargeImage, which does not need a new rendering window (instead of vtkWindowToImageFilter).
    """
    import vtk

    if large_image:
        w2if = vtk.vtkRenderLargeImage()
        w2if.SetMagnification(mag)  # => multiply the resolution of the picture
        w2if.SetInput(renderer)
        w2if.Update()
    else:
        renWin = vtk.vtkRenderWindow() # --- Rendering windows
        renWin.SetOffScreenRendering(1)
        renWin.AddRenderer(renderer)
        if size is None: 
            size = renWin.GetSize()
        renWin.SetSize( mag*size[0], mag * size[1] )
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(renWin)
        w2if.Update() # .Modified

    w = writerFromExt(pictureFile[-4:])()
    w.SetFileName(pictureFile)
    w.SetInputConnection(w2if.GetOutputPort())
    w.Write()

    logger.debug(f"{pictureFile:} written")


def vtk_show(renderer, size = (800.,600.)):
    """Takes vtkRenderer instance and returns an IPython Image with the rendering.

    To be used in jupyter notebook to vizualize a vtk image.
    """
    import vtk
    from IPython.display import Image
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetOffScreenRendering(1)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize( *size )
    renderWindow.Render()

    windowToImageFilter = vtk.vtkWindowToImageFilter()
    windowToImageFilter.SetInput(renderWindow)
    windowToImageFilter.Update()

    writer = vtk.vtkPNGWriter()
    writer.SetWriteToMemory(1)
    writer.SetInputConnection(windowToImageFilter.GetOutputPort())
    writer.Write()
    data = memoryview(writer.GetResult()).tobytes()

    return Image(data)



#For backward compatibility
def viewPolyData( polydata, *args,**kwargs):
    VtkLite.FromPolydata( polydata, *args,**kwargs ).to_interactive()


def pictureFromSingleVtk( vtkFile, picture_file, **kwargs ):
    """Set camera positon

    Parameters
    ----------
    vtkFile : str
        The vtk file
    pictureFile : str
        Output picture name
    camSettings : dict, optional
        Camera settings
    """
    
    VtkLite.FromVtuFile( vtkFile, **kwargs ).to_picture(picture_file)
    
