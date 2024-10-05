import os

from pydantic import BaseModel, Field

OpenAiApiKey = Field(
    None,
    title="OpenAI API Key",
    examples=["sk-1234567890abcdef"],
    json_schema_extra={
        "help": "Create an account and find your API key at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys) to get an API key."
    },
)


class BaseEnvVars(BaseModel):

    @classmethod
    def get_issues(cls):
        issues = []
        for field_name, field in cls.model_fields.items():
            if field.default is None and os.getenv(field_name) is None:
                msg = f"Missing required environment variable: {field_name}"
                if field.json_schema_extra.get("help"):
                    msg += f" ({field.json_schema_extra.get('help')})"
                issues.append(msg)
        return issues

    @classmethod
    def to_desc(cls):
        if cls.model_fields:
            prefix = "You will need the following API key"
            if len(cls.model_fields) > 1:
                prefix += "s"
            prefix += ":"
            return (
                "\n".join(
                    [
                        f"* **{field_name}**: {field.json_schema_extra.get('help')}"
                        for field_name, field in cls.model_fields.items()
                    ]
                )
                + "\n\nAPI keys are added from [tryplurally.com/studio](https://tryplurally.com/studio#api-keys?addKey=1)"
            )
        return ""
