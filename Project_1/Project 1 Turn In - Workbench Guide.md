# MCD FCFF Workbench

Run this product from the repository root:

```powershell
python ".\MCD Research\mcd_workbench.py"
```

It uses only the Python standard library. A small window opens; no web server, package installation, or account is required.

## What is locked

- The five-year three-statement accounting engine in `mcd_project1_fcff.py`.
- Base-year inputs, the source/provenance record, enterprise-to-equity bridge, and all articulation checks.
- FCFF definition: NOPAT + depreciation - capex - inventory investment - other working-capital investment.

## What an analyst can adjust

| Driver | Base | Bounded range | Why this range is exposed |
|---|---:|---:|---|
| FY2026--FY2030 revenue growth | 4.0%, 4.0%, 3.5%, 3.0%, 2.5% | 0%--6% each year | Growth is a load-bearing judgment; bounds keep the view within a defensible mature-company range. |
| Gross margin | 59.51% | 58%--61% | Anchored to the FY2025 franchise-led analytical margin. |
| WACC | 7.05% | 6%--8% | Captures a reasonable valuation-input challenge without allowing arbitrary discount rates. |
| Terminal growth | 2.50% | 2%--9%, and below WACC | Long-run growth must remain below WACC for a valid Gordon-growth terminal value. |

The detailed value, basis, challenge, and changing evidence for each load-bearing driver are in the Assumptions and Source Map and the Edition B memo.

## Required demo

Use **Calculate** after moving a bounded driver, read the updated valuation and sensitivity, then use **Reset base**. Use **Demo failing check** to deliberately set terminal growth above WACC: the workbench displays a red failure rather than a misleading valuation. Click **Reset base** again to recover.
