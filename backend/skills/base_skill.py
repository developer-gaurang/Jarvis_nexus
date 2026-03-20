class BaseSkill:
    name = "BaseSkill"
    description = "A generic backend skill interface."

    def can_handle(self, user_input: str) -> bool:
        """Determines if this skill should intercept the user's input."""
        return False

    def execute(self, user_input: str, context: dict) -> str:
        """Executes the skill's logic."""
        raise NotImplementedError("Skills must implement the 'execute' method.")
