import logging

logger = logging.getLogger()

def register_worker_commands(cli):
    @cli.command()
    def worker():
        from mtmai.flows.article_gen import flow_article_gen

        flow_article_gen.serve(name="flow-article-gen",
                      tags=["mtmai","article-gen"],
                      webserver=True,
                      parameters={"goodbye": True},

                    #   interval=120,
                      )

        print("启动 worker")
