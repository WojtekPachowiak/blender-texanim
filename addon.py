import bpy
import bgl
import gpu
from gpu_extras.presets import draw_texture_2d

WIDTH = None
HEIGHT = None




def get_viewport_width_height():
    global WIDTH, HEIGHT
    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            for r in a.regions:
                if r.type == 'WINDOW':
                    WIDTH = r.width
                    HEIGHT = r.height
#                    print(f"Viewport dimensions: {r.width}x{r.height}, approximate aspect rato: {round(r.width/r.height, 2)}")

def draw():
    context = bpy.context
    scene = context.scene

    view_matrix = scene.camera.matrix_world.inverted()

    projection_matrix = scene.camera.calc_matrix_camera(
        context.evaluated_depsgraph_get(), x=WIDTH, y=HEIGHT)

    offscreen.draw_view3d(
        scene,
        context.view_layer,
        context.space_data,
        context.region,
        view_matrix,
        projection_matrix)

    bgl.glDisable(bgl.GL_DEPTH_TEST)
    draw_texture_2d(offscreen.color_texture, (0, 0), WIDTH, HEIGHT)


get_viewport_width_height()
offscreen = gpu.types.GPUOffScreen(WIDTH, HEIGHT)
h = bpy.types.SpaceView3D.draw_handler_add(draw, (), 'WINDOW', 'POST_PIXEL')

def rm_handler():
    global h
    print("Hello World")
    bpy.types.SpaceView3D.draw_handler_remove(h, 'WINDOW')
    
bpy.app.timers.register(rm_handler, first_interval=15)
