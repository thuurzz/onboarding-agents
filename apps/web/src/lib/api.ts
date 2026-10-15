export const AGENTS_API_URL =
  process.env.NEXT_PUBLIC_AGENTS_API_URL ?? "http://localhost:8002";

export const MOCK_GEMUD_API_URL =
  process.env.NEXT_PUBLIC_MOCK_GEMUD_API_URL ?? "http://localhost:8001";

export interface ChatRequest {
  message: string;
  thread_id?: string | null;
}

export interface ChatResponse {
  thread_id: string;
  reply: string;
  ticket_result: Record<string, unknown> | null;
}

export interface Ticket {
  id?: number | null;
  platform: string;
  nome_coordenacao: string;
  centro_custo: string;
  matricula_responsavel: string;
  fields: Record<string, unknown>;
  created_at?: string | null;
}

export async function sendChatMessage(
  message: string,
  threadId?: string | null,
): Promise<ChatResponse> {
  const body: ChatRequest = { message, thread_id: threadId ?? null };

  const res = await fetch(`${AGENTS_API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error(`Falha ao conversar com o agente (${res.status}).`);
  }

  return (await res.json()) as ChatResponse;
}

export async function listTickets(): Promise<Ticket[]> {
  const res = await fetch(`${MOCK_GEMUD_API_URL}/tickets`);

  if (!res.ok) {
    throw new Error(`Falha ao listar tickets (${res.status}).`);
  }

  return (await res.json()) as Ticket[];
}
