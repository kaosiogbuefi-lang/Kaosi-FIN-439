"""Semi-adjustable MCD FCFF workbench; uses only Python's standard library."""

import tkinter as tk
from tkinter import ttk

import mcd_project1_fcff as model


BASE = {
    "growth": [0.040, 0.040, 0.035, 0.030, 0.025],
    "gross_margin": 0.5951,
    "wacc": model.weighted_average_cost_of_capital(),
    "terminal_growth": 0.025,
}


class Workbench(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MCD Project 1 — FCFF Workbench")
        self.geometry("1060x780")
        self.growth_vars = [tk.DoubleVar(value=value * 100) for value in BASE["growth"]]
        self.margin_var = tk.DoubleVar(value=BASE["gross_margin"] * 100)
        self.wacc_var = tk.DoubleVar(value=BASE["wacc"] * 100)
        self.terminal_var = tk.DoubleVar(value=BASE["terminal_growth"] * 100)
        self.status_var = tk.StringVar(value="Ready — base assumptions loaded.")
        self._build()
        self.calculate()

    def _build(self):
        controls = ttk.LabelFrame(self, text="Bounded driver panel — edit assumptions, then click Calculate")
        controls.pack(fill="x", padx=10, pady=8)
        for index, var in enumerate(self.growth_vars):
            ttk.Label(controls, text=f"FY{2026 + index} revenue growth (0%–6%)").grid(row=index, column=0, sticky="w", padx=6, pady=2)
            ttk.Scale(controls, from_=0.0, to=6.0, variable=var, orient="horizontal", length=310).grid(row=index, column=1, padx=6, pady=2)
            ttk.Label(controls, textvariable=var, width=7).grid(row=index, column=2, sticky="w")
        drivers = [
            ("Gross margin (58%–61%)", self.margin_var, 58.0, 61.0),
            ("WACC (6%–8%)", self.wacc_var, 6.0, 8.0),
            ("Terminal growth (2%–9%; must be below WACC)", self.terminal_var, 2.0, 9.0),
        ]
        for offset, (label, var, low, high) in enumerate(drivers):
            row = offset * 2
            ttk.Label(controls, text=label).grid(row=row, column=3, sticky="w", padx=12, pady=2)
            ttk.Scale(controls, from_=low, to=high, variable=var, orient="horizontal", length=260).grid(row=row, column=4, padx=6, pady=2)
            ttk.Label(controls, textvariable=var, width=7).grid(row=row, column=5, sticky="w")
        buttons = ttk.Frame(controls)
        buttons.grid(row=6, column=0, columnspan=6, sticky="w", padx=6, pady=8)
        ttk.Button(buttons, text="Calculate", command=self.calculate).pack(side="left", padx=3)
        ttk.Button(buttons, text="Reset base", command=self.reset_base).pack(side="left", padx=3)
        ttk.Button(buttons, text="Demo failing check", command=self.demo_failure).pack(side="left", padx=3)

        ttk.Label(self, textvariable=self.status_var, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=14)
        self.output = tk.Text(self, height=25, width=130, wrap="none", font=("Consolas", 10))
        self.output.pack(fill="both", expand=True, padx=10, pady=8)
        self.output.tag_configure("pass", foreground="#0b6e27")
        self.output.tag_configure("fail", foreground="#b00020")

    def assumptions(self):
        return (
            [var.get() / 100.0 for var in self.growth_vars],
            self.margin_var.get() / 100.0,
            self.wacc_var.get() / 100.0,
            self.terminal_var.get() / 100.0,
        )

    def write(self, text, tag=None):
        self.output.insert("end", text + "\n", tag)

    def calculate(self):
        growth, margin, wacc, terminal = self.assumptions()
        self.output.delete("1.0", "end")
        try:
            result = model.dcf_value(growth, wacc, terminal, margin)
            rows = result["rows"]
            self.status_var.set("CHECKS PASS — coherent input combination.")
            self.write("MCD FCFF WORKBENCH — visible analyst output")
            self.write(f"Growth path: {', '.join(f'{value:.2%}' for value in growth)}")
            self.write(f"Gross margin: {margin:.2%}; WACC: {wacc:.2%}; terminal growth: {terminal:.2%}")
            self.write("")
            self.write(f"Value per diluted share: ${result['per_share']:.2f}")
            self.write(f"Enterprise value: ${result['enterprise_value']:,.1f}M")
            self.write(f"Terminal-value share of EV: {result['terminal_share']:.1%}")
            self.write(f"Reverse-DCF reference price: ${model.market_price:.2f}")
            self.write("")
            self.write("Checks", "pass")
            for row in rows:
                self.write(f"FY{row['year']}E balance gap {row['balance_gap']:.1f}; cash-flow tie gap {row['cash_tie_gap']:.1f}", "pass")
            self.write("")
            self.write("One-at-a-time revenue-growth sensitivity")
            for label, shift in [("Low", -0.01), ("Base", 0.0), ("High", 0.01)]:
                scenario = model.dcf_value([value + shift for value in growth], wacc, terminal, margin)
                self.write(f"{label}: ${scenario['per_share']:.2f} per share")
            self.write("")
            self.write("WACC / terminal-growth sensitivity")
            rates = [wacc - 0.005, wacc, wacc + 0.005]
            terminal_rates = [max(0.0, terminal - 0.005), terminal, terminal + 0.005]
            self.write("WACC \\ g      " + "  ".join(f"{rate:.1%}" for rate in terminal_rates))
            for rate in rates:
                cells = []
                for growth_rate in terminal_rates:
                    if growth_rate >= rate:
                        cells.append("invalid")
                    else:
                        cells.append(f"${model.dcf_value(growth, rate, growth_rate, margin)['per_share']:.2f}")
                self.write(f"{rate:.2%}      " + "  ".join(cells))
        except ValueError as error:
            self.status_var.set(f"CHECK FAILED — {error}")
            self.write("CHECK FAILED — incoherent input combination.", "fail")
            self.write(str(error), "fail")
            self.write("Use Reset base to restore a coherent set of assumptions.", "fail")

    def reset_base(self):
        for var, value in zip(self.growth_vars, BASE["growth"]):
            var.set(value * 100)
        self.margin_var.set(BASE["gross_margin"] * 100)
        self.wacc_var.set(BASE["wacc"] * 100)
        self.terminal_var.set(BASE["terminal_growth"] * 100)
        self.calculate()

    def demo_failure(self):
        self.terminal_var.set(self.wacc_var.get() + 0.5)
        self.calculate()


if __name__ == "__main__":
    Workbench().mainloop()
