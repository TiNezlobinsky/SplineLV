import os
import vtk
from SplineMeasurement.engine.interactor_style import InteractorPointPicker
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


# CODE REGIONS:
# 1) Initialization
# 2) Setters
# 3) Getters
# 4) Scene updating
# 5) Scene elements


class VtkMeasScene(QVTKRenderWindowInteractor):
    def __init__(self, parent=None):
        QVTKRenderWindowInteractor.__init__(self, parent)

        self._objects_count = 0
        self._objects_list = []
        self._renderer_list = []
        self._scene_elements_list = []

        self._current_slice_number = 0
        self._current_slice = None
        self._current_renderer = None
        self._current_scene_elements_dict = None

        self._files_format = ""

# INITIALIZATION:

    def initialize_window(self):
        self._render = vtk.vtkRenderer()
        self.GetRenderWindow().AddRenderer(self._render)
        self._interactor = self.GetRenderWindow().GetInteractor()
        self._interactor_style = InteractorPointPicker()
        self._interactor_style.SetDefaultRenderer(self._render)
        self._interactor.SetInteractorStyle(self._interactor_style)
        self._interactor.Initialize()

    def initialize_scene(self):
        if self._renderer_list:
            self.clear_scene()
        for i in range(self._objects_count):
            self._renderer_list.append(vtk.vtkRenderer())
            if self._files_format == "image":
                scene_element = self._create_image_scene_element()
            elif self._files_format == "mesh":
                scene_element = self._create_mesh_scene_element()

            self._scene_elements_list.append(scene_element)
            self._bind_scene_element_to_renderer(self._renderer_list[-1],
                                                 self._scene_elements_list[-1]["actor"])

        self._interactor_style.set_object_type(self._files_format)
        self._interactor_style.set_vtk_observers()

# SETTERS:

    def set_files_format(self, form):
        self._files_format = form

    def set_files_type(self, type_str):
        self._files_format = type_str

    def set_objects_count(self, count):
        self._objects_count = count

    def set_objects_list(self, objects_list):
        self._objects_list = objects_list

    def set_current_scene_frame(self, i):
        # called when object list was switched
        self._current_slice_number = i
        self._current_slice = self._objects_list[i]
        self._current_renderer = self._renderer_list[i]
        self._current_scene_elements_dict = self._scene_elements_list[i]
        self._update_references(self._current_slice, self._current_renderer, self._current_scene_elements_dict)
        self._interactor.Initialize()

    def set_object(self, i, object_):
        # calls when object was transformed
        self._objects_list[i] = object_
        self._current_slice = object_
        self._update_references(self._current_slice, self._current_renderer, self._current_scene_elements_dict)
        self._interactor.Initialize()

# GETTERS:

    def get_interactor(self):
        return self._interactor

    def get_interactor_style(self):
        return self._interactor_style

    def get_renderer_list(self):
        return self._renderer_list

    def get_renderer(self, i):
        return self._renderer_list[i]

    def get_scene_elements_list(self):
        return self._scene_elements_list

    def get_current_slice_number(self):
        return self._current_slice_number

# SCENE UPDATING:

    def _update_references(self, slice_, renderer, scene_elements_dict):
        self._set_main_renderer(renderer)
        self._set_main_slice(slice_, renderer, *scene_elements_dict.values())
        self._interactor_style.SetDefaultRenderer(renderer)

    def _set_main_slice(self, slice_, renderer, mapper, actor):
        mapper.SetInputData(slice_)
        renderer.RemoveActor(actor)
        if self._files_format == "image":
            actor.SetInputData(mapper.GetInput())
        else:
            actor.SetMapper(mapper)
        renderer.AddActor(actor)
        renderer.ResetCamera()

    def _set_main_renderer(self, renderer):
        self.GetRenderWindow().RemoveRenderer(renderer)
        self.GetRenderWindow().AddRenderer(renderer)

# SCENE ELEMENTS:

    def _create_image_scene_element(self):
        mapper = vtk.vtkImageMapper()
        actor = vtk.vtkImageActor()
        return {"mapper": mapper, "actor": actor}

    def _create_mesh_scene_element(self):
        mapper = vtk.vtkDataSetMapper()
        actor = vtk.vtkActor()
        return {"mapper": mapper, "actor": actor}

    def _bind_scene_element_to_renderer(self, renderer, actor):
        renderer.AddActor(actor)

    def clear_scene(self):
        """
        Remove all elements from the scene
        """
        self._scene_elements_list = []
        for renderer in self._renderer_list:
            renderer.RemoveAllViewProps()
