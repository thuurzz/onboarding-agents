from langgraph.graph import END, START, StateGraph

from app.controllers import graph as nodes
from app.models.state import OnboardingState


def build_graph(checkpointer=None):
    workflow = StateGraph(OnboardingState)

    workflow.add_node("porteiro", nodes.porteiro)
    workflow.add_node("especialista", nodes.especialista)
    workflow.add_node("validador", nodes.validador)
    workflow.add_node("abrir_ticket", nodes.abrir_ticket_node)

    workflow.add_edge(START, "porteiro")
    workflow.add_conditional_edges(
        "porteiro",
        nodes.route_after_porteiro,
        {"especialista": "especialista", "end": END},
    )
    workflow.add_edge("especialista", "validador")
    workflow.add_conditional_edges(
        "validador",
        nodes.route_after_validador,
        {"especialista": "especialista", "abrir_ticket": "abrir_ticket", "end": END},
    )
    workflow.add_edge("abrir_ticket", END)

    return workflow.compile(checkpointer=checkpointer)
