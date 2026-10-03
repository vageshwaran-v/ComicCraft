def build_comic_layout(outline, story, image_paths):
    layout = []

    for index in range(len(outline)):
        panel = outline[index]
        story_panel = story[index]

        layout.append({
            "panel_number": panel["panel_number"],
            "title": panel["title"],
            "scene_description": panel["scene_description"],
            "image_prompt": panel["image_prompt"],
            "image_path": image_paths[index],
            "caption": story_panel["caption"],
            "narration": story_panel["narration"],
            "dialogue": story_panel["dialogue"]
        })

    return layout