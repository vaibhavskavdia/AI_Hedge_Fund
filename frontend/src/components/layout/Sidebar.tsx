import { NavLink } from "react-router-dom";
import {
  BriefcaseBusiness,
  Building2,
  ChartCandlestick,
  
  Sparkles,
} from "lucide-react";

const navigation = [
  {
    name: "Portfolio",
    href: "/",
    icon: BriefcaseBusiness,
  },
  {
    name: "Research",
    href: "/research",
    icon: Sparkles,
  },
  {
    name: "Stocks",
    href: "/stocks",
    icon: ChartCandlestick,
  },
  {
    name: "Sectors",
    href: "/sectors",
    icon: Building2,
  },
  
];

export default function Sidebar() {
  return (
    <aside className="hidden w-72 shrink-0 border-r border-slate-800 bg-slate-950 lg:flex lg:flex-col">
      {/* Logo */}
      <div className="border-b border-slate-800 px-8 py-8">
        <div className="flex items-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-blue-600">
            <ChartCandlestick className="h-6 w-6 text-white" />
          </div>

          <div>
            <h1 className="text-lg font-semibold tracking-tight text-white">
              AI Hedge Fund
            </h1>

            <p className="mt-1 text-sm text-slate-400">
              Institutional Platform
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6">
        <div className="space-y-2">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.href}
                className={({ isActive }) =>
                  [
                    "group flex items-center gap-3 rounded-xl px-4 py-3 transition-all duration-200",
                    isActive
                      ? "bg-slate-900 text-white"
                      : "text-slate-400 hover:bg-slate-900/60 hover:text-white",
                  ].join(" ")
                }
              >
                <Icon className="h-5 w-5" />

                <span className="text-sm font-medium">{item.name}</span>
              </NavLink>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      <div className="border-t border-slate-800 p-6">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4">
          <p className="text-xs uppercase tracking-[0.2em] text-slate-500">
            Status
          </p>

          <div className="mt-3 flex items-center gap-2">
            <div className="h-2 w-2 rounded-full bg-green-500" />

            <span className="text-sm text-slate-300">
              Backend Connected
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}