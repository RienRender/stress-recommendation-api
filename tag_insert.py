from src.services.tag_service import get_or_create_tag

tags = ["breathing", "meditation", "walking", "relaxation"]

for t in tags:
    get_or_create_tag(t, "mindfulness", "global")