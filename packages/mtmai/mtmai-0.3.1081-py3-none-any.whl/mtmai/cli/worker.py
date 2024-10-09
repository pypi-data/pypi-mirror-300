import logging

from prefect import deploy

logger = logging.getLogger()

def register_worker_commands(cli):
    @cli.command()
    def worker():
        from mtmai.flows.article_gen import flow_article_gen

        # flow_article_gen.serve(name="flow-article-gen",
        #               tags=["mtmai","article-gen"],
        #               webserver=True,
        #               parameters={"goodbye": True},

        #             #   interval=120,
        #               )

        deploy(
          # Use the `to_deployment` method to specify configuration
          #specific to each deployment
          flow_article_gen.to_deployment("my-deployment-1"),
          # my_flow_2.to_deployment("my-deployment-2"),

          # Specify shared configuration for both deployments
          # image="my-docker-image:dev",
          push=False,
          work_pool_name="my-work-pool",
      )

        print("启动 worker")
