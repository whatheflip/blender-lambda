import bpy
import bpy.utils.previews
import os
from bpy.app.handlers import persistent
# from PIL import Image


import sys
import time

start_time = time.time()



arguments = {}


if len(sys.argv) > 1:
    
    for arg in sys.argv[1:]:
        
        arg_parts = arg.split('=')
        if len(arg_parts) == 2:
            key, value = arg_parts
            arguments[key] = value


def str_to_bool(value):
    return value.lower() in ['true', 'yes', '1']


sna_input_frames = arguments.get('INPUT_FRAMES', None)
sna_input_cover = arguments.get('INPUT_COVER', None)
sna_cover_filename = arguments.get('COVER_FILENAME', None)
sna_output_pre_render = arguments.get('OUTPUT_PRE_RENDER', None)
sna_output_final_video = arguments.get('OUTPUT_FINAL_VIDEO', None)
sna_text_front = arguments.get('TEXT_FRONT', None)
sna_text_side = arguments.get('TEXT_SIDE', None)
sna_text_back = arguments.get('TEXT_BACK', None)
sna_base_frames = arguments.get('BASE_FRAMES', None)
sna_color_cover = arguments.get('COLOR_COVER', None)
sna_color_text = arguments.get('COLOR_TEXT', None)
sna_color_background = arguments.get('COLOR_BACKGROUND', None)
sna_output_pre_render_trash = arguments.get('OUTPUT_PRE_RENDER_TRASH', None)
# sna_sequence_type_video = arguments.get('SEQUENCE_TYPE_VIDEO', None)
sna_sequence_type_video = str_to_bool(arguments.get('SEQUENCE_TYPE_VIDEO', 'false'))

#sna_sequence_type_video = str_to_bool(arguments.get('SEQUENCE_TYPE_VIDEO', 'false'))



if sna_input_frames is not None and sna_input_cover is not None and sna_cover_filename is not None and sna_output_pre_render is not None and sna_output_final_video is not None and sna_text_front is not None and sna_text_side is not None and sna_text_back is not None and sna_base_frames is not None and sna_color_cover is not None and sna_color_text is not None and sna_color_background is not None and sna_output_pre_render_trash is not None and sna_sequence_type_video is not None:



    auto_render = {'sna_udim_gallery_list': [], 'sna_input_frames': sna_input_frames, 'sna_input_cover': sna_input_cover, 'sna_cover_filename': sna_cover_filename, 'sna_output_pre_render': sna_output_pre_render, 'sna_output_final_video': sna_output_final_video, 'sna_text_front': sna_text_front, 'sna_text_side': sna_text_side, 'sna_text_back': sna_text_back, 'sna_base_frames': sna_base_frames, 'sna_color_cover': sna_color_cover, 'sna_color_text': sna_color_text, 'sna_color_background': sna_color_background, 'sna_output_pre_render_trash': sna_output_pre_render_trash, 'sna_sequence_type_video': sna_sequence_type_video }




    def enable_gpus(device_type):
        preferences = bpy.context.preferences
        cycles_preferences = preferences.addons["cycles"].preferences
        cycles_preferences.refresh_devices()
        devices = cycles_preferences.devices
        if not devices:
            raise RuntimeError("Unsupported device type")
        activated_gpus = []
        for device in devices:
            if device.type == "CPU":
                device.use = False
                print('Activated CPU:', device.name)
            else:
                device.use = True
                activated_gpus.append(device.name)
                print('Activated GPU:', device.name)
        cycles_preferences.compute_device_type = device_type
        # bpy.context.preferences.addons['cycles'].preferences.compute_device_type = "OPTIX"
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.cycles.device = "GPU"
        prefs = bpy.context.preferences.addons['cycles'].preferences
        print('Cycles Render Device: ', bpy.context.preferences.addons['cycles'].preferences.compute_device_type)
        print('Render Engine: ', bpy.context.scene.render.engine)
        print('Render Device: ', bpy.context.scene.cycles.device)
        return activated_gpus
    # enable_gpus("OPTIX")
    input_frames = os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])

    def rename_frames(directory):
        files = os.listdir(directory)
        files.sort()
        count = 1001
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.exr'):
                new_name = 'Page.{:04d}'.format(count) + os.path.splitext(file)[1]
                old_path = os.path.join(directory, file)
                new_path = os.path.join(directory, new_name)
                os.rename(old_path, new_path)
                count += 1
    directory_path = input_frames
    rename_frames(directory_path)
    input_frames = os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])

    def reduce_resolution(input_folder, max_side_length):
        for filename in os.listdir(input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(input_folder, filename)
                with Image.open(image_path) as img:
                    width, height = img.size
                    if width >= height:
                        new_width = max_side_length
                        new_height = int(height * (max_side_length / width))
                    else:
                        new_width = int(width * (max_side_length / height))
                        new_height = max_side_length
                    resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    resized_img.save(image_path)
                    print(f"{filename} resized and saved to {image_path}")
    input_folder = input_frames
    max_side_length = 600
    # reduce_resolution(input_folder, max_side_length)
    bpy.context.view_layer.objects['Book_text'].hide_render = False
    bpy.context.scene.view_layers['Book'].use = False
    bpy.context.scene.view_layers['Pages'].use = True
    hex_color = auto_render['sna_color_background']
    rgba_color = None
    r = None
    g = None
    b = None
    a = None
    # Convert hex color code to RGB values
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    # Combine RGB values and alpha value to create RGBA color
    r, g, b = [c / 255.0 for c in rgb_color]
    alpha = 1
    rgba_color = (r, g, b, alpha)
    # Extract individual RGBA values
    r, g, b, a = rgba_color
    # Print RGBA values
    #print(f"R = {r}")
    #print(f"G = {g}")
    #print(f"B = {b}")
    #print(f"A = {a}")
    bpy.data.materials['Backplane'].node_tree.nodes['backplane_color'].outputs[0].default_value = rgba_color
    hex_color = auto_render['sna_color_cover']
    rgba_color = None
    r = None
    g = None
    b = None
    a = None
    # Convert hex color code to RGB values
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    # Combine RGB values and alpha value to create RGBA color
    r, g, b = [c / 255.0 for c in rgb_color]
    alpha = 1
    rgba_color = (r, g, b, alpha)
    # Extract individual RGBA values
    r, g, b, a = rgba_color
    # Print RGBA values
    #print(f"R = {r}")
    #print(f"G = {g}")
    #print(f"B = {b}")
    #print(f"A = {a}")
    bpy.data.materials['Flipbook_cover'].node_tree.nodes['Flipbook_cover_color'].outputs[0].default_value = rgba_color
    hex_color = auto_render['sna_color_text']
    rgba_color = None
    r = None
    g = None
    b = None
    a = None
    # Convert hex color code to RGB values
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
    # Combine RGB values and alpha value to create RGBA color
    r, g, b = [c / 255.0 for c in rgb_color]
    alpha = 1
    rgba_color = (r, g, b, alpha)
    # Extract individual RGBA values
    r, g, b, a = rgba_color
    # Print RGBA values
    #print(f"R = {r}")
    #print(f"G = {g}")
    #print(f"B = {b}")
    #print(f"A = {a}")
    bpy.data.materials['Flipbook_text'].node_tree.nodes['Flipbook_text_color'].outputs[0].default_value = rgba_color
    bpy.context.scene.node_tree.nodes['Compositor_BG_color'].outputs['RGBA'].default_value = rgba_color
    bpy.data.materials['Flipbook_pages'].node_tree.nodes['PAGES_WHITE_SWITCH'].inputs[0].default_value = 0.0
    for i_7CF88 in range(len(bpy.data.images)-1,-1,-1):
        if 'UDIM' in str(bpy.data.images[i_7CF88].name_full):
            bpy.data.images.remove(image=bpy.data.images[i_7CF88], )
    frames_list = [f for f in os.listdir(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])))) if os.path.isfile(os.path.join(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames']))), f))]
    frames_list_cleaned = None
    frames_list_cleaned = []
    frames_list.sort()
    for file in frames_list:
        if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('.exr'):
            frames_list_cleaned.append(file)
            print(file)
    print(frames_list_cleaned)
    #return(frames_list_cleaned)
    bpy.ops.image.open('INVOKE_DEFAULT', filepath=os.path.join(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames']))),sorted(frames_list_cleaned, reverse=False)[0]), use_udim_detecting=True)
    input_string = os.path.basename(os.path.join(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames']))),sorted(frames_list_cleaned, reverse=False)[0])).replace(os.path.splitext(os.path.join(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames']))),sorted(frames_list_cleaned, reverse=False)[0]))[1], '')
    output_string = None

    def replace_numbers_with_test(string):
        # Iterate backwards through the string
        i = len(string) - 1
        while i >= 0 and string[i].isdigit():
            i -= 1
        # If we found digits at the end of the string, replace them with "TEST"
        if i != len(string) - 1:
            return string[:i+1]
        else:
            return string
    # Example usage
    #input_string = "hel23lo1234"
    output_string = replace_numbers_with_test(input_string)
    #print(output_string)  # Output: helloTEST
    print(output_string + '<UDIM>' + os.path.splitext(os.path.join(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames']))),sorted(frames_list_cleaned, reverse=False)[0]))[1])
    material_name = 'Flipbook_pages'
    image_node_name = 'Flipbook_pages_image'
    new_image_name = output_string + '<UDIM>' + os.path.splitext(os.path.join(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_frames']))),sorted(frames_list_cleaned, reverse=False)[0]))[1]
    # Get the image node
    image_node = bpy.data.materials[material_name].node_tree.nodes.get(image_node_name)
    if image_node:
        # Get the reference to the new image
        new_image = bpy.data.images.get(new_image_name)
        if new_image:
            # Assign the new image to the image node
            image_node.image = new_image
            print("Image replaced successfully.")
        else:
            print("New image not found.")
    else:
        print("Image node not found.")
    bpy.ops.image.open('INVOKE_DEFAULT', filepath=os.path.join(os.path.dirname(os.path.join(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_cover']),auto_render['sna_cover_filename'])),os.path.basename(os.path.join(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_cover']),auto_render['sna_cover_filename']))))
    material_name = 'Flipbook_cover'
    image_node_name = 'Flipbook_cover_image'
    new_image_name = os.path.basename(os.path.join(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_input_cover']),auto_render['sna_cover_filename']))
    # Get the image node
    image_node = bpy.data.materials[material_name].node_tree.nodes.get(image_node_name)
    if image_node:
        # Get the reference to the new image
        new_image = bpy.data.images.get(new_image_name)
        if new_image:
            # Assign the new image to the image node
            image_node.image = new_image
            print("Image replaced successfully.")
        else:
            print("New image not found.")
    else:
        print("Image node not found.")
    multiline_string = auto_render['sna_text_front']
    result = None

    def add_pipe_every_eighth(text):
        length = len(text)
        if length < 8:
            return text
        else:
            new_text = ""
            for i in range(length):
                new_text += text[i]
                if (i + 1) % 8 == 0 and i != length - 1:
                    new_text += "|"
            return new_text
    input_string = multiline_string
    result = add_pipe_every_eighth(input_string)
    bpy.data.objects['dynamic_text1'].modifiers['GeometryNodes']['Socket_2'] = result
    bpy.data.objects['dynamic_text2'].modifiers['GeometryNodes']['Socket_2'] = auto_render['sna_text_side']
    bpy.data.objects['dynamic_text3'].modifiers['GeometryNodes']['Socket_2'] = auto_render['sna_text_back']
    bpy.context.view_layer.objects['dynamic_text1'].data.update()
    bpy.context.view_layer.objects['dynamic_text2'].data.update()
    bpy.context.view_layer.objects['dynamic_text3'].data.update()
    print(os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_output_pre_render'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_output_pre_render']))))
    image_folder_import_path = os.path.join(os.path.dirname(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_output_pre_render'])),os.path.basename(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_output_pre_render'])))
    fps = 25

    def get_image_files(image_folder_path, image_extension=".exr"):
        image_files = list()
        for file_name in os.listdir(image_folder_path):
            if file_name.endswith(image_extension):
                image_files.append(file_name)
        image_files.sort()
        print(image_files)
        return image_files

    def add_compositor_nodes(image_sequence, duration):
        """
        Find the Compositor Nodes we need here
        https://docs.blender.org/api/current/bpy.types.CompositorNode.html#bpy.types.CompositorNode
        """
        scene = bpy.context.scene
        compositor_node_tree = scene.node_tree
        #bpy.data.scenes["Scene"]
        #bpy.context.scene.node_tree.nodes['base_layers_image']
        #image_node = compositor_node_tree.nodes("base_layers_image")
        image_node = bpy.context.scene.node_tree.nodes['base_layers_image2']
        image_node.image = image_sequence
        image_node.frame_duration = duration
        image_node.frame_start = 1
        image_node.frame_offset = 0
        #composite_node = compositor_node_tree.nodes['base_layers_image']
        #composite_node.location.x = 200
        #viewer_node = compositor_node_tree.nodes.new(type="CompositorNodeViewer")
        #viewer_node.location.x = 200
        #viewer_node.location.y = -200
        # create links
        #compositor_node_tree.links.new(image_node.outputs["Image"], composite_node.inputs["Image"])
        #compositor_node_tree.links.new(image_node.outputs["Image"], viewer_node.inputs["Image"])

    def import_image_sequence_into_compositor(image_folder_path, fps):
        image_files = get_image_files(image_folder_path)
        file_info = list()
        for image_name in image_files:
            file_info.append({"name": image_name})
        bpy.ops.image.open(directory=image_folder_path, files=file_info)
        scene = bpy.context.scene
        scene.use_nodes = True
        #remove_compositor_nodes()
        image_data_name = image_files[0]
        image_sequence = bpy.data.images[image_data_name]
        duration = len(image_files)
        add_compositor_nodes(image_sequence, duration)
        #scene.frame_end = duration
        #width, height = image_sequence.size
        #scene.render.resolution_y = height
        #scene.render.resolution_x = width
        #scene.render.fps = fps
    image_folder_path = image_folder_import_path
    import_image_sequence_into_compositor(image_folder_path, fps)
    bpy.data.scenes['Scene'].node_tree.nodes['Compositor_image_switch'].check = True
    if auto_render['sna_sequence_type_video']:
        bpy.data.scenes['Scene'].render.image_settings.file_format = 'FFMPEG'
        bpy.data.scenes['Scene'].render.ffmpeg.format = 'WEBM'
        bpy.data.scenes['Scene'].render.ffmpeg.codec = 'WEBM'
        bpy.data.scenes['Scene'].render.ffmpeg.constant_rate_factor = 'PERC_LOSSLESS'
        bpy.data.scenes['Scene'].render.ffmpeg.ffmpeg_preset = 'GOOD'
    else:
        bpy.data.scenes['Scene'].render.image_settings.file_format = 'PNG'
        bpy.data.scenes['Scene'].render.image_settings.color_mode = 'RGB'
        bpy.data.scenes['Scene'].render.image_settings.color_depth = '8'
        bpy.data.scenes['Scene'].render.image_settings.compression = 0
        bpy.data.scenes['Scene'].render.use_overwrite = True
    bpy.data.scenes['Scene'].render.engine = 'CYCLES'
    bpy.data.scenes['Scene'].cycles.use_adaptive_sampling = False
    bpy.data.scenes['Scene'].cycles.samples = 1
    bpy.data.scenes['Scene'].cycles.max_bounces = 1
    bpy.data.scenes['Scene'].cycles.diffuse_bounces = 1
    bpy.data.scenes['Scene'].cycles.glossy_bounces = 1
    bpy.data.scenes['Scene'].cycles.transmission_bounces = 0
    bpy.data.scenes['Scene'].cycles.volume_bounces = 0
    bpy.data.scenes['Scene'].cycles.transparent_max_bounces = 0
    bpy.data.scenes['Scene'].cycles.sample_clamp_direct = 1.0
    bpy.data.scenes['Scene'].cycles.sample_clamp_indirect = 10.0
    bpy.data.scenes['Scene'].render.use_motion_blur = False
    bpy.data.scenes['Scene'].render.motion_blur_shutter = 0.5
    bpy.data.scenes['Scene'].render.use_persistent_data = True
    bpy.data.scenes['Scene'].render.resolution_x = 444
    bpy.data.scenes['Scene'].render.resolution_y = 586
    bpy.data.scenes['Scene'].render.resolution_percentage = 100
    bpy.context.scene.render.fps = 25
    bpy.data.scenes['Scene'].frame_start = 1
    bpy.data.scenes['Scene'].frame_end = int(240 * float(25 / 30))
    bpy.data.scenes['Scene'].render.frame_map_new = int(float(25 / 30) * 100.0)
    bpy.data.scenes['Scene'].render.filepath = os.path.join(os.path.join(os.path.dirname(bpy.data.filepath),auto_render['sna_output_final_video']),'flipbook_preview_')
    bpy.context.scene.node_tree.nodes['FILE_OUTPUT'].mute = True
    bpy.data.scenes['Scene'].view_settings.view_transform = 'Standard'
    bpy.data.scenes['Scene'].view_settings.look = 'None'
    print("FINISHED")


    end_time = time.time()

    duration = end_time - start_time
    print("Script execution time:", duration, "seconds")