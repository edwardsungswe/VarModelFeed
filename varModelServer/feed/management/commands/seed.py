from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime


class Command(BaseCommand):
    help = 'Seed the database with mock users and posts (feed)'

    def handle(self, *args, **options):
        from user.models import User
        from feed.models import Post

        mock_users = [
            {"email": "edward@varmodel.com", "password": "password123", "name": "Edward Sung"},
            {"email": "jane@abao.co", "password": "password123", "name": "Jane Kim"},
            {"email": "alex@basetech.io", "password": "password123", "name": "Alex Chen"},
        ]

        user_map = {}
        for u in mock_users:
            obj, created = User.objects.update_or_create(
                email=u["email"], defaults={"name": u["name"], "password_hash": u["password"]}
            )
            user_map[u["email"]] = obj
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} user: {obj.email}")

        mock_posts = [
            {
                "company_name": "PrecisionMarketing.io",
                "logo_placeholder": "PM",
                "title": "Content Marketing Partnership",
                "description": 'Content marketing boosts awareness of "Your AI" before that a concept after it has captured its maximum partnership.',
                "detailed_description": (
                    "PrecisionMarketing.io is seeking strategic partners to co-develop content marketing campaigns that leverage AI-driven insights. "
                    "Our platform analyzes audience behavior in real-time and generates targeted content recommendations. We are looking for partners with strong content creation capabilities who want to integrate AI-powered analytics into their workflow. "
                    "Together, we can create campaigns that are both data-driven and creatively compelling, reaching the right audiences at the right time."
                ),
                "images": [
                    "https://picsum.photos/seed/pm1/800/600",
                    "https://picsum.photos/seed/pm2/800/600",
                    "https://picsum.photos/seed/pm3/800/600",
                ],
                "videos": [
                    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                ],
                "created_at": "2025-12-01T10:00:00Z",
            },
            {
                "company_name": "ABAO Company",
                "logo_placeholder": "AB",
                "title": "Development Partnership",
                "description": "The purpose of this company, based in the current city, is to drive your developer or more opps in building AI/LLI.",
                "detailed_description": (
                    "ABAO Company specializes in building developer tools and SDKs for AI and large language model integration. We are looking for development partners who can help us expand our ecosystem of plugins and integrations. "
                    "Our platform currently supports Python and JavaScript, and we want to extend support to Go, Rust, and other languages. Partners will have early access to our API, co-marketing opportunities, and revenue sharing on jointly developed products."
                ),
                "images": [
                    "https://picsum.photos/seed/abao1/800/600",
                    "https://picsum.photos/seed/abao2/800/600",
                ],
                "videos": [
                    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
                ],
                "created_at": "2025-11-28T14:30:00Z",
            },
            {
                "company_name": "BASE Technology",
                "logo_placeholder": "BASE",
                "title": "Authentication Partnership",
                "description": "Dynamic authentication utility of this. Want that this opened focuses to convenient versatile accustoms to for professionals.",
                "detailed_description": (
                    "BASE Technology provides enterprise-grade authentication and identity management solutions. We are seeking partners to integrate our passwordless authentication SDK into their applications. Our solution supports biometrics, hardware keys, and magic links, reducing friction for end users while maintaining high security standards. "
                    "Partners benefit from reduced support costs related to password resets and improved user onboarding conversion rates."
                ),
                "images": [
                    "https://picsum.photos/seed/base1/800/600",
                    "https://picsum.photos/seed/base2/800/600",
                    "https://picsum.photos/seed/base3/800/600",
                    "https://picsum.photos/seed/base4/800/600",
                ],
                "videos": [],
                "created_at": "2025-11-25T09:15:00Z",
            },
        ]

        # helper to choose author by company name
        def choose_author_for_company(company_name):
            name = company_name.lower()
            if "abao" in name:
                return user_map.get("jane@abao.co")
            if "base" in name:
                return user_map.get("alex@basetech.io")
            return user_map.get("edward@varmodel.com")

        for p in mock_posts:
            author = choose_author_for_company(p["company_name"])
            created = parse_datetime(p["created_at"]) or None
            obj, was_created = Post.objects.update_or_create(
                title=p["title"], company_name=p["company_name"],
                defaults={
                    "logo_placeholder": p["logo_placeholder"],
                    "description": p["description"],
                    "detailed_description": p["detailed_description"],
                    "images": p["images"],
                    "videos": p["videos"],
                    "created_at": created,
                    "author": author,
                },
            )
            action = "Created" if was_created else "Updated"
            self.stdout.write(f"{action} post: {obj.title} (author={obj.author})")

        self.stdout.write(self.style.SUCCESS("Seeding complete."))
