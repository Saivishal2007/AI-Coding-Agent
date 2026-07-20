class GenerationPipeline:

    def __init__(

        self,

        planner,

        generator,

        reviewer,

        executor,

    ):

        self.planner = planner

        self.generator = generator

        self.reviewer = reviewer

        self.executor = executor