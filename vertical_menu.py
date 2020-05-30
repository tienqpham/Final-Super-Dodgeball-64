import pygame

# an external event handler is required to activate selected menu item
# use VerticalMenu.get_selected() to retrieve selected item
# use VerticalMenu.get_joystick() to retrieve supported joystick
class VerticalMenu():
    
    # PARAMETERS:
    # rect:
    #   a pygame.Rect defining the position and boundaries of the menu
    # items_off:
    #   a list of images for each item's unselected state
    # items_on:
    #   a list of images for each item's selected state
    # center_spacing:
    #   TRUE: the distance bewteen adjacent items' centers is fixed;
    #         this setting is default and advisable for images of
    #         different sizes
    #   FALSE: the distance between an item's bottom edge and the
    #          next item's top edge is fixed
    # joystick: represents the ID of a joystick used to navigate this menu;
    #           -2 to negative infinity uses all joysticks
    #           -1 uses no joysticks
    #           0 to infinity uses the joystick of that ID
    # uses_keyboard:
    #   TRUE: the menu can be navigated with the keyboard
    #   FALSE: the menu cannot be navigated with the keyboard
    # uses_mouse:
    #   TRUE: the menu can be navigated with the mouse
    #   FALSE: the menu cannot be navigated with the mouse
    
    # PRECONDITIONS:
    # items_off and items_on must be of the same length
    def __init__(self, rect, items_off, items_on, joystick=-2,
                 uses_keyboard=True, uses_mouse=True, center_spacing = True):

        self.joysticks = []
        if joystick <= -2:
            for i in range(0,pygame.joystick.get_count()):
                pygame.joystick.Joystick(i).init()
                self.joysticks.append(pygame.joystick.Joystick(i))
        elif joystick >= 0:
            if joysticks >= pygame.joystick.get_count():
                raise ValueError("joystick of ID does not exist")
            pygame.joystick.Joystick(i).init()
            self.joysticks.append(pygame.joystick.Joystick(i))
        
        self.center_spacing = center_spacing

        if len(items_off) != len(items_on):
            #throw an error
            raise ValueError("Unequal length of items_off and items_on")

        
        
        self.items_on = items_on
        self.items_off = items_off
        
        self.rect = rect

        self.height = rect.size[1]
        self.width = rect.size[0]
        
        self.top = rect.y
        self.bottom = self.top + self.height
        self.left = rect.x
        self.right = self.left + self.width
        
        self.item_width = items_on[0].get_rect().size[0]
        self.item_height = items_on[0].get_rect().size[1]
        
        for item in items_on:
            if item.get_rect().size[0] > self.item_width:
                self.item_width = item.get_rect().size[0]
            if item.get_rect().size[1] > self.item_height:
                self.item_height = item.get_rect().size[1]

        self.length = len(items_off)

        if self.center_spacing:
            self.positions = []
            vertical_gap = self.height / (self.length+1)
            for i in range (0,self.length):
                self.positions.append( (self.width/2+self.left, self.top+vertical_gap*(i+1)) )
                

        self.gap_x = ( self.width - self.item_width ) /2
        self.gap_y = ( self.height - self.item_height * self.length) / (self.length + 1)

        self.selected_item = -1

        self.uses_keyboard = uses_keyboard
        self.uses_mouse = uses_mouse

        self.mouse_is_visible = False
        if self.uses_mouse:
            self.mouse_is_visible = True

    # resets menu so no item is selected
    def reset(self, reset_point = -1):
        self.selected_item = reset_point

    # retrieves index of currently selected item
    # returns between 0 and length-1 if an item is selected
    # returns -1 if no item is selected
    def get_selected(self):
        return self.selected_item

    # returns the number of items in the menu
    def get_length(self):
        return self.length

    # moves item selection up one item in the list
    def cursor_up(self):
        if self.selected_item > 0:
            self.selected_item -= 1
        elif self.selected_item == -1:
            self.selected_item = 0

    # moves item selection down one item in the list
    def cursor_down(self):
        if self.selected_item < self.length - 1:
            self.selected_item += 1

    def update(self):
        self.check_mouse()
        self.set_mouse_visibility()
        if self.center_spacing:
            for i in range (0,self.length):
                rect = self.items_off[i].get_rect(center=self.positions[i])
            
                if rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_is_visible:
                    self.selected_item = i

        elif not self.center_spacing:
            for i in range (0,self.length):
                item_width = self.items_on[i].get_rect().size[0]
                item_height = self.items_on[i].get_rect().size[1]

                gap_x = ( self.width - item_width ) /2
                gap_y = ( self.height - item_height * self.length) / (self.length + 1)
            
                rect = pygame.Rect(gap_x + self.left,
                                   gap_y * (i+1) + item_height * i + self.top,
                                   item_width,
                                   item_height)
            
                if rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_is_visible:
                    self.selected_item = i

    def draw(self, screen):
        if self.center_spacing:
            for i in range (0, self.length):
                rect = self.items_off[i].get_rect(center=self.positions[i])
                
                if self.selected_item == i:
                    screen.blit(self.items_on[i], (rect.x,rect.y) )
                else:
                    screen.blit(self.items_off[i], (rect.x,rect.y) )

        elif not self.center_spacing:
            for i in range (0,self.length):
                item_width = self.items_on[i].get_rect().size[0]
                item_height = self.items_on[i].get_rect().size[1]

                gap_x = ( self.width - item_width ) /2
                gap_y = ( self.height - item_height * self.length) / (self.length + 1)

                coord = [gap_x + self.left,
                         gap_y * (i+1) + item_height * i + self.top]
                if self.selected_item == i:
                    screen.blit(self.items_on[i], coord)
                else:
                    screen.blit(self.items_off[i], coord)
                    
            

    def check_mouse(self):
        if pygame.mouse.get_rel() != (0,0) and self.uses_mouse:
                self.mouse_is_visible = True

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.uses_keyboard:
            self.mouse_is_visible = False
            if event.key == pygame.K_w or event.key==pygame.K_UP:
                self.cursor_up()
            elif event.key == pygame.K_s or event.key==pygame.K_DOWN:
                self.cursor_down()
            elif event.key == pygame.K_SPACE:
                print("button " + str(self.selected_item + 1) + " pressed")
        if event.type == pygame.JOYHATMOTION:
            for joystick in self.joysticks:
                if joystick.get_hat(0)[1] == 1:
                    self.cursor_up()
                if joystick.get_hat(0)[1] == -1:
                    self.cursor_down()
        if event.type == pygame.MOUSEBUTTONDOWN and self.mouse_is_visible:
            if pygame.mouse.get_pressed()[0]:
                print("button " + str(self.selected_item + 1) + " pressed")
