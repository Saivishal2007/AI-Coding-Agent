class IntentClassifierService:
    """
    Determines how the agent should handle a request.
    """

    CHAT = "chat"

    REPOSITORY_QUERY = "repository_query"

    MODIFY_REPOSITORY = "modify_repository"

    REVIEW_CODE = "review_code"

    DEBUG_CODE = "debug_code"

    EXPLAIN_CODE = "explain_code"

    SECURITY_REVIEW = "security_review"

    PERFORMANCE_REVIEW = "performance_review"

    def classify(
        self,
        prompt: str,
    ) -> str:

        prompt = prompt.lower()

        # -------------------------
        # Review
        # -------------------------

        review_keywords = [

            "review",

            "code review",

            "inspect",

            "analyze",

            "find issues",

            "find bugs",

            "check code",

        ]

        for keyword in review_keywords:

            if keyword in prompt:

                return self.REVIEW_CODE

        # -------------------------
        # Debug
        # -------------------------

        debug_keywords = [

            "debug",

            "bug",

            "error",

            "exception",

            "crash",

            "not working",

            "fails",

        ]

        for keyword in debug_keywords:

            if keyword in prompt:

                return self.DEBUG_CODE

        # -------------------------
        # Security
        # -------------------------

        security_keywords = [

            "security",

            "vulnerability",

            "sql injection",

            "xss",

            "csrf",

            "audit",

        ]

        for keyword in security_keywords:

            if keyword in prompt:

                return self.SECURITY_REVIEW

        # -------------------------
        # Performance
        # -------------------------

        performance_keywords = [

            "performance",

            "optimize",

            "optimization",

            "speed",

            "slow",

        ]

        for keyword in performance_keywords:

            if keyword in prompt:

                return self.PERFORMANCE_REVIEW

        # -------------------------
        # Explain
        # -------------------------

        explain_keywords = [

            "explain",

            "understand",

            "how does",

            "what does",

        ]

        for keyword in explain_keywords:

            if keyword in prompt:

                return self.EXPLAIN_CODE

        # -------------------------
        # Repository Query
        # -------------------------

        repository_keywords = [

            "repository",

            "project",

            "service",

            "class",

            "function",

            "file",

            "folder",

        ]

        for keyword in repository_keywords:

            if keyword in prompt:

                return self.REPOSITORY_QUERY

        # -------------------------
        # Modification
        # -------------------------

        modification_keywords = [

            "create",

            "build",

            "edit",

            "modify",

            "update",

            "refactor",

            "fix",

            "delete",

            "rename",

            "implement",

            "add",

        ]

        for keyword in modification_keywords:

            if keyword in prompt:

                return self.MODIFY_REPOSITORY

        return self.CHAT