import importlib
import pkgutil
import skills

class SkillManager:
    def __init__(self):
        self.skills = {}
        self.load_skills()

    def load_skills(self):
        """Dynamically load all skills from the `skills` package."""
        for _, module_name, _ in pkgutil.iter_modules(skills.__path__):
            module = importlib.import_module(f'skills.{module_name}')
            for attribute_name in dir(module):
                attribute = getattr(module, attribute_name)
                # Register class if it has a specific base class/interface
                if isinstance(attribute, type) and hasattr(attribute, "can_handle") and attribute.__name__ != "BaseSkill":
                    skill_instance = attribute()
                    self.skills[skill_instance.name] = skill_instance
                    print(f"[Core] Loaded skill: {skill_instance.name}")

    def handle_intent(self, intent: str, context: dict):
        """Route intent to the appropriate skill."""
        for name, skill in self.skills.items():
            if skill.can_handle(intent):
                return skill.execute(intent, context)
        return None
