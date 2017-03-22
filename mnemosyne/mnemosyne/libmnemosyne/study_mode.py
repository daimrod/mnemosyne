#
# study_mode.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.component import Component


class StudyMode(Component):
    
    """A study mode is a collection of a scheduler and a review controller. 
    Different study modes can share e.g. the same scheduler, but instantiated
    with different parameters.
    
    Each study more should also have a review widget, indicated through the
    'gui_for_component' mechanism.
    
    """

    id = "" 
    name = ""
    menu_weight = 0 # To determine sorting order in menu
    component_type = "study_mode"
    Scheduler = None  # Class
    ReviewController = None  # Class
    
    def activate_components(self):
        self.component_manager.register(\
            self.Scheduler(self.component_manager))
        self.log().started_scheduler()
        self.component_manager.register(\
            self.ReviewController(self.component_manager))
        for component in self.gui_components:
            component = component(component_manager=self.component_manager) 
            self.component_manager.register(component)
            component.activate()
       
    def activate(self):
        print("activate study mode", self)        
        Component.activate(self)
        self.activate_components()
        self.review_controller().reset()
        
    def deactivate(self):
        print("deactivate study mode", self)
        Component.deactivate(self)
        self.scheduler().deactivate()
        self.component_manager.unregister(self.scheduler())
        self.review_controller().deactivate()
        self.component_manager.unregister(self.review_controller())
