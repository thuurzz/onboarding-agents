"use client";

import { useEffect, useState } from "react";
import { listTickets, type Ticket } from "@/lib/api";

export default function TicketsTab() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setError(null);
    try {
      setTickets(await listTickets());
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro inesperado.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium text-zinc-700">
          Tickets criados
        </h2>
        <button
          onClick={load}
          disabled={loading}
          className="rounded-lg border border-zinc-300 px-3 py-1.5 text-sm text-zinc-700 transition-colors hover:bg-zinc-50 disabled:opacity-50"
        >
          {loading ? "Atualizando..." : "Atualizar"}
        </button>
      </div>

      {error && (
        <p className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </p>
      )}

      {loading && tickets.length === 0 ? (
        <p className="text-sm text-zinc-500">Carregando tickets...</p>
      ) : tickets.length === 0 ? (
        <p className="text-sm text-zinc-500">Nenhum ticket encontrado.</p>
      ) : (
        <ul className="space-y-3">
          {tickets.map((ticket) => (
            <li
              key={ticket.id ?? `${ticket.platform}-${ticket.centro_custo}`}
              className="rounded-lg border border-zinc-200 bg-white p-4 shadow-sm"
            >
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-zinc-900">
                  {ticket.platform}
                </span>
                {ticket.id != null && (
                  <span className="text-xs text-zinc-400">#{ticket.id}</span>
                )}
              </div>

              <dl className="mt-2 grid grid-cols-1 gap-1 text-sm text-zinc-700 sm:grid-cols-2">
                <div className="flex flex-col">
                  <dt className="text-xs text-zinc-500">Coordenação</dt>
                  <dd>{ticket.nome_coordenacao}</dd>
                </div>
                <div className="flex flex-col">
                  <dt className="text-xs text-zinc-500">Centro de custo</dt>
                  <dd>{ticket.centro_custo}</dd>
                </div>
                <div className="flex flex-col">
                  <dt className="text-xs text-zinc-500">Matrícula responsável</dt>
                  <dd>{ticket.matricula_responsavel}</dd>
                </div>
                {ticket.created_at && (
                  <div className="flex flex-col">
                    <dt className="text-xs text-zinc-500">Criado em</dt>
                    <dd>{new Date(ticket.created_at).toLocaleString("pt-BR")}</dd>
                  </div>
                )}
              </dl>

              {ticket.fields && Object.keys(ticket.fields).length > 0 && (
                <div className="mt-2 border-t border-zinc-100 pt-2">
                  <p className="text-xs font-medium text-zinc-500">Campos adicionais</p>
                  <dl className="mt-1 grid grid-cols-1 gap-1 text-sm text-zinc-700 sm:grid-cols-2">
                    {Object.entries(ticket.fields).map(([key, value]) => (
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
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
