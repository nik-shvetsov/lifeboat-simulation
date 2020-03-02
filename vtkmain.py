import vtk

filenameBoat = "data\\LIVbaat2.stl"
filenameWaterSTL = "data\\water.stl"
# filenameWater = "data\\w3.txt"
filenameWater = "data\\water200.txt"
filenameCover = "data\\covernew2.txt"

# ######################for texture##########################
# tex = "D:\\images.jpg"
# readertex = vtk.vtkJPEGReader()
# readertex.SetFileName(tex)
# texture = vtk.vtkTexture()
# texture.SetInputConnection(readertex.GetOutputPort())
############################################################

# readers
readerSTL = vtk.vtkSTLReader()
readerSTL.SetFileName(filenameBoat)
# reader.Update()

readerWSTL = vtk.vtkSTLReader()
readerWSTL.SetFileName(filenameWaterSTL)

readerP = vtk.vtkParticleReader()
readerP.SetFileName(filenameWater)  # filenameWater #filenameCover
readerP.SetDataByteOrderToBigEndian()
readerP.Update()

# mappers
mapperSTL = vtk.vtkPolyDataMapper()
mapperSTL.SetInputConnection(readerSTL.GetOutputPort())

mapperWSTL = vtk.vtkPolyDataMapper()
mapperWSTL.SetInputConnection(readerWSTL.GetOutputPort())

mapperP = vtk.vtkPolyDataMapper()
mapperP.SetInputConnection(readerP.GetOutputPort())
mapperP.SetScalarRange(0.0, 999.9)  # (0.0, 999.9) #(0.1, 1.0)

# actors
actorSTL = vtk.vtkActor()
actorSTL.SetMapper(mapperSTL)
# color the actor
actorSTL.GetProperty().SetColor(1, 0.64, 0)  # (R,G,B)
actorSTL.SetPosition(14.75, 0, 0.1)  # (14,0,0)
# actorSTL.SetOrigin(7.5,0,0)
# actorSTL.SetScale(0.9)
# actorSTL.RotateY(1.0)
stlPos = actorSTL.GetPosition()
print("STL pos:", stlPos)

actorWSTL = vtk.vtkActor()
actorWSTL.SetMapper(mapperWSTL)
# color the actor
actorWSTL.GetProperty().SetColor(0.4, 0.56, 0.9)  # (R,G,B)
# actorWSTL.SetPosition(15,0,0)


actorP = vtk.vtkActor()
actorP.SetMapper(mapperP)
actorP.GetProperty().SetPointSize(5)  # 4
pPos = actorP.GetPosition()
print("P pos:", pPos)


# clipper actors---------------------------------------------------
# particles clipper
clipPlane = vtk.vtkPlane()
clipPlane.SetNormal(0.0, -1.0, 0)
clipPlane.SetOrigin(0.0, 0.0, 0.0)

clipperP = vtk.vtkClipPolyData()
clipperP.SetInputConnection(readerP.GetOutputPort())
clipperP.SetClipFunction(clipPlane)

clipMapperP = vtk.vtkPolyDataMapper()
clipMapperP.SetInputConnection(clipperP.GetOutputPort())
clipMapperP.SetScalarRange(0.0, 999.9)

clipActorP = vtk.vtkActor()
clipActorP.SetMapper(clipMapperP)
clipActorP.GetProperty().SetPointSize(8)  # 4
# clipActorP.SetPosition()

# STL clipper
clipperSTL = vtk.vtkClipPolyData()
clipperSTL.SetInputConnection(readerSTL.GetOutputPort())
clipperSTL.SetClipFunction(clipPlane)

clipMapperSTL = vtk.vtkPolyDataMapper()
clipMapperSTL.SetInputConnection(clipperSTL.GetOutputPort())

clipActorSTL = vtk.vtkActor()
clipActorSTL.SetMapper(clipMapperSTL)
clipActorSTL.SetPosition(stlPos)
# clipActorSTL.RotateY(-1.0)
clipActorSTL.GetProperty().SetColor(actorSTL.GetProperty().GetColor())

# WSTL clipper
clipperWSTL = vtk.vtkClipPolyData()
clipperWSTL.SetInputConnection(readerWSTL.GetOutputPort())
clipperWSTL.SetClipFunction(clipPlane)

clipMapperWSTL = vtk.vtkPolyDataMapper()
clipMapperWSTL.SetInputConnection(clipperWSTL.GetOutputPort())

clipActorWSTL = vtk.vtkActor()
clipActorWSTL.SetMapper(clipMapperWSTL)
clipActorWSTL.GetProperty().SetColor(0.4, 0.56, 0.9)

# ---------------------------------------------------------
# backFaces = vtk.vtkProperty()
# backFaces.SetSpecular(0.0)
# backFaces.SetDiffuse(0.0)
# backFaces.SetAmbient(1.0)
# backFaces.SetAmbientColor(1.0000, 0.3882, 0.2784)
# clipActorSTL.SetBackfaceProperty(backFaces)
# ---------------------------------------------------------

# cutter#######################################################
plane = vtk.vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0, 1, 0)

cutter = vtk.vtkCutter()
cutter.SetCutFunction(plane)
cutter.SetInputConnection(readerSTL.GetOutputPort())
cutter.Update()

FeatureEdges = vtk.vtkFeatureEdges()
FeatureEdges.SetInputConnection(cutter.GetOutputPort())
FeatureEdges.BoundaryEdgesOn()
FeatureEdges.FeatureEdgesOff()
FeatureEdges.NonManifoldEdgesOff()
FeatureEdges.ManifoldEdgesOff()
FeatureEdges.Update()

cutStrips = vtk.vtkStripper()  # Forms loops (closed polylines) from cutter
cutStrips.SetInputConnection(cutter.GetOutputPort())
cutStrips.Update()
cutPoly = vtk.vtkPolyData()  # This trick defines polygons as polyline loop
cutPoly.SetPoints((cutStrips.GetOutput()).GetPoints())
cutPoly.SetPolys((cutStrips.GetOutput()).GetLines())

cutterMapper = vtk.vtkPolyDataMapper()
cutterMapper.SetInputConnection(cutter.GetOutputPort())
cutterMapper.SetInputData(cutPoly)

# create plane actor
planeActor = vtk.vtkActor()
planeActor.GetProperty().SetColor(1.0, 1.0, 0.0)
planeActor.GetProperty().SetEdgeColor(1.0, 0.0, 0.0)
planeActor.GetProperty().SetLineWidth(2)
planeActor.GetProperty().EdgeVisibilityOn()
# planeActor.GetProperty().SetOpacity(0.7)
planeActor.SetMapper(cutterMapper)
planeActor.SetPosition(stlPos)


def main():
    # One render window, multiple viewports
    # renderWindowInteractor_list = []
    renderWindow = vtk.vtkRenderWindow()
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # renderWindowInteractor.SetInteractorStyle(
    # vtk.vtkInteractorStyleTrackballCamera())

    # Define viewport ranges
    xmins = [0.01, 0.51, 0.01, 0.51]
    xmaxs = [0.49, 0.99, 0.49, 0.99]
    ymins = [0.01, 0.01, 0.51, 0.51]
    ymaxs = [0.49, 0.49, 0.99, 0.99]

    for i in range(4):
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(1, 1, 1)

        # renderer.SetBackgroundTexture(texture)
        # renderer.SetTexturedBackground(True)

        renderWindow.AddRenderer(renderer)
        renderer.SetViewport(xmins[i], ymins[i], xmaxs[i], ymaxs[i])

        # renderer.AddActor(actorSTL)
        # renderer.AddActor(actorP)
        # renderer.AddActor(actorWSTL)
        renderer.AddActor(clipActorP)
        renderer.AddActor(clipActorSTL)
        renderer.AddActor(clipActorWSTL)
        renderer.AddActor(planeActor)

        # stPos = renderer.GetActiveCamera().GetPosition()
        # focPoint = renderer.GetActiveCamera().GetFocalPoint()
        # print("Pos", stPos)
        # print ("Foc point", focPoint)

        # default
        renderer.ResetCamera()

        if (i == 0):  # from back (3rd quarter)
            renderer.GetActiveCamera().SetFocalPoint(stlPos)
            renderer.GetActiveCamera().SetPosition(stlPos[0] + 10.0,
                                                   stlPos[1], stlPos[2])
            renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
            renderer.ResetCamera()

        if (i == 1):  # from bottom (4rd quarter)
            renderer.GetActiveCamera().SetFocalPoint(stlPos)
            renderer.GetActiveCamera().SetPosition(stlPos[0], stlPos[1],
                                                   stlPos[2] - 10.0)
            renderer.GetActiveCamera().SetViewUp(0.0, 1.0, 0.0)
            renderer.ResetCamera()

        if (i == 2):  # from front (2nd quarter)
            renderer.GetActiveCamera().SetFocalPoint(stlPos)
            renderer.GetActiveCamera().SetPosition(stlPos[0] - 10.0, stlPos[1],
                                                   stlPos[2])
            renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
            renderer.ResetCamera()

    scalar_bar = vtk.vtkScalarBarActor()
    scalar_bar.SetOrientationToHorizontal()

    # scalar_bar.SetWidth(0.05)
    # scalar_bar.SetHeight(0.5)
    scalar_bar.SetTitle("Density")
    scalar_bar.GetTitleTextProperty().SetColor(0, 0, 0)

    scalar_bar.SetNumberOfLabels(5)
    scalar_bar.SetLabelFormat('%.1f')  # ("%+#6.2e")
    scalar_bar.SetLookupTable(clipActorP.GetMapper().GetLookupTable())
    # scalar_bar.SetLookupTable(actorP.GetMapper().GetLookupTable())
    scalar_bar.GetLabelTextProperty().SetFontFamilyToCourier()
    scalar_bar.GetLabelTextProperty().SetJustificationToRight()
    scalar_bar.GetLabelTextProperty().SetVerticalJustificationToCentered()
    scalar_bar.GetLabelTextProperty().BoldOn()
    scalar_bar.GetLabelTextProperty().ItalicOff()
    scalar_bar.GetLabelTextProperty().ShadowOff()
    scalar_bar.GetLabelTextProperty().SetColor(0, 0, 0)

    # create the scalar bar widget
    scalar_bar_widget = vtk.vtkScalarBarWidget()
    scalar_bar_widget.SetInteractor(renderWindowInteractor)
    scalar_bar_widget.SetScalarBarActor(scalar_bar)
    scalar_bar_widget.On()

    renderWindow.SetSize(1870, 900)
    renderWindow.Render()
    renderWindow.SetWindowName('Lifeboat visualization')
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()
