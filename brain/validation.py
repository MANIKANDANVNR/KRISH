class ResponseValidator:

    def validate(self, response):

        if not isinstance(
            response,
            str,
        ):
            raise ValueError(
                "Response must be text."
            )

        response = response.strip()

        if not response:
            raise ValueError(
                "Model returned empty response."
            )

        return response