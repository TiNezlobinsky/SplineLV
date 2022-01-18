from vtk import vtkInteractorStyleImage, vtkCoordinate


class InteractorPointPicker(vtkInteractorStyleImage):
    def __init__(self,):
        self._change_contrast_on = False

        self._object_type = ""

        self._point_position = None

    def set_object_type(self, obj_type):
        self._object_type = obj_type

    def set_vtk_observers(self):
        if self._object_type == "image":
            self.AddObserver("LeftButtonPressEvent", self._leftButtonPressEvent_image)
            self.AddObserver("RightButtonPressEvent", self._leftButtonPressEvent_image)
            self.AddObserver("LeftButtonPressEvent", self._change_contrast)
        elif self._object_type == "mesh":
            self._coordinate = vtkCoordinate()
            self.AddObserver("LeftButtonPressEvent", self._leftButtonPressEvent_mesh)
            self.AddObserver("RightButtonPressEvent", self._leftButtonPressEvent_mesh)

    def _change_contrast(self, obj, event):
        if self._change_contrast_on:
            vtkInteractorStyleImage.OnLeftButtonDown(self)
        else:
            # switching off image contrast change (it takes place if you use vtkInteractorStyleImage)
            pass

    def contrast_on(self):
        self._change_contrast_on = True

    def contrast_off(self):
        self._change_contrast_on = False

    def _leftButtonPressEvent_image(self, obj, event):
        position = self.GetInteractor().GetEventPosition()
        self.GetInteractor().GetPicker().Pick(position[0], position[1], 1, self.GetDefaultRenderer())
        self._point_position = self.GetInteractor().GetPicker().GetPickPosition()
        return

    def _leftButtonPressEvent_mesh(self, obj, event):
        position = self.GetInteractor().GetEventPosition()
        self._coordinate.SetCoordinateSystemToDisplay()
        self._coordinate.SetValue(position[0], position[1], 0)
        self._point_position = self._coordinate.GetComputedWorldValue(self.GetDefaultRenderer())
        return

    def get_picked_position(self):
        return self._point_position
