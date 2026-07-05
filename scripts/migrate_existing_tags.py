from src.config.supabase_client import supabase
from src.services.tag_service import get_or_create_tag, attach_tags_to_activity

def migrate():

    activities = supabase.table("activities").select("*").execute().data

    for activity in activities:
        activity_id = activity["id"]

        # 👇 IMPORTANT: adjust this depending on your column
        raw_tags = activity.get("tags", [])

        if not raw_tags:
            continue

        tag_ids = []

        for tag in raw_tags:
            tag_id = get_or_create_tag(
                tag_name=tag,
                activity_type=activity.get("activity_type", "general"),
                source="global"
            )
            tag_ids.append(tag_id)

        attach_tags_to_activity(activity_id, tag_ids)

        print(f"✅ Migrated tags for activity {activity_id}")

if __name__ == "__main__":
    migrate()