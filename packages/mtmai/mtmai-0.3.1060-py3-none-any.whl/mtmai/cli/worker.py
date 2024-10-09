import logging

logger = logging.getLogger()

def register_worker_commands(cli):
    @cli.command()
    def worker():
        from mtmai.flows.hello_flow import flow_hello
        flow_hello.serve(name="my-deployment2",
                      tags=["onboarding"],
                      parameters={"goodbye": True},
                      interval=120)

        print("启动 worker")