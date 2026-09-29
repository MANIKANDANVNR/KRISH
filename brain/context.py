class ContextBuilder:

    def build(
        self,
        system_prompt,
        conversation,
        memories,
        user_input,
    ):

        messages = []

        if system_prompt:

            messages.append({
                "role": "system",
                "content": system_prompt,
            })

        for message in conversation:

            messages.append({
                "role": message["role"],
                "content": message["content"],
            })

        if memories:

            memory_text = "\n".join(
                f"- {memory}"
                for memory in memories
            )

            messages.append({
                "role": "system",
                "content":
                    "Relevant memory:\n"
                    + memory_text,
            })

        messages.append({
            "role": "user",
            "content": user_input,
        })

        return messages