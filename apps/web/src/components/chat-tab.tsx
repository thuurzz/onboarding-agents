"use client";

import { useState } from "react";
import {
  sendChatMessage,
  type ChatResponse,
  type Ticket,
} from "@/lib/api";

export default function ChatTab() {
  const [message, setMessage] = useState("");
  const [threadId, setThreadId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [responses, setResponses] = useState<ChatResponse[]>([]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = message.trim();
    if (!trimmed || loading) return;

    setLoading(true);
    setError(null);

    try {
      const res = await sendChatMessage(trimmed, threadId);
      setThreadId(res.thread_id);
      setResponses((prev) => [...prev, res]);
      setMessage("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="flex flex-col gap-2">
          <label htmlFor="message" className="text-sm font-medium text-zinc-700">
            Mensagem
          </label>
          <textarea
            id="message"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Descreva o que você precisa para o agente de onboarding..."
            rows={3}
            className="w-full rounded-lg border border-zinc-300 px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-500 focus:outline-none"
          />
        </div>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={loading || !message.trim()}
            className="rounded-lg bg-zinc-900 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-zinc-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? "Enviando..." : "Enviar"}
          </button>

          {threadId && (
            <span className="text-xs text-zinc-500">
              Conversa: {threadId.slice(0, 8)}...
            </span>
          )}
        </div>

        {error && (
          <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </p>
        )}
      </form>

      <div className="space-y-4">
        {responses.length === 0 && !loading && (
          <p className="text-sm text-zinc-500">
            Nenhuma conversa ainda. Envie uma mensagem para começar.
          </p>
        )}

        {responses.map((res, i) => (
          <div
            key={i}
            className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm"
          >
            <p className="whitespace-pre-wrap text-sm text-zinc-800">
              {res.reply}
            </p>

            {res.ticket_result && (
              <TicketCard ticket={res.ticket_result} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

function TicketCard({ ticket }: { ticket: Record<string, unknown> }) {
  return (
    <div className="mt-3 rounded-lg border border-green-200 bg-green-50 p-3">
      <p className="text-xs font-semibold uppercase tracking-wide text-green-700">
        Ticket criado
      </p>
      <dl className="mt-2 grid grid-cols-1 gap-1 text-sm text-zinc-700 sm:grid-cols-2">
        {Object.entries(ticket).map(([key, value]) => (
          <div key={key} className="flex flex-col">
            <dt className="text-xs text-zinc-500">{key}</dt>
            <dd className="break-words">
              {typeof value === "object" && value !== null
                ? JSON.stringify(value)
                : String(value ?? "—")}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}
