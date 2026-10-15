"use client";

import { useState } from "react";
import ChatTab from "@/components/chat-tab";
import TicketsTab from "@/components/tickets-tab";

type Tab = "chat" | "tickets";

export default function Home() {
  const [tab, setTab] = useState<Tab>("chat");

  return (
    <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-6 py-8">
      <header className="flex flex-col gap-1">
        <h1 className="text-2xl font-semibold tracking-tight text-zinc-900">
          Onboarding de Agentes
        </h1>
        <p className="text-sm text-zinc-500">
          Converse com o agente e acompanhe os tickets criados.
        </p>
      </header>

      <nav className="flex gap-1 border-b border-zinc-200">
        {(
          [
            ["chat", "Chat"],
            ["tickets", "Tickets"],
          ] as const
        ).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            className={`-mb-px border-b-2 px-4 py-2 text-sm font-medium transition-colors ${
              tab === key
                ? "border-zinc-900 text-zinc-900"
                : "border-transparent text-zinc-500 hover:text-zinc-700"
            }`}
          >
            {label}
          </button>
        ))}
      </nav>

      {tab === "chat" ? <ChatTab /> : <TicketsTab />}
    </div>
  );
}
