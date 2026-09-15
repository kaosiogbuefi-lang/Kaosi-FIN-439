"""Lab 07 Asbury P/E comparison; uses only Python's standard library."""

# Editable frozen training-case inputs.
target = {"ticker": "ABG", "price": 243.03, "diluted_eps": 21.50}
peers = [
    {"ticker": "AN", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "price": 421.48, "diluted_eps": 36.81},
]


def valid_positive_number(value):
    return isinstance(value, (int, float)) and value > 0


def usable_peers(target_data, peer_data):
    """Deduplicate tickers, exclude the target, and retain usable P/E inputs."""
    target_ticker = target_data["ticker"].upper()
    seen, usable, rejected = set(), [], []
    for peer in peer_data:
        ticker = peer["ticker"].upper()
        if ticker == target_ticker:
            rejected.append((ticker, "target excluded"))
        elif ticker in seen:
            rejected.append((ticker, "duplicate excluded"))
        elif not valid_positive_number(peer["price"]) or not valid_positive_number(peer["diluted_eps"]):
            rejected.append((ticker, "P/E not meaningful: price or EPS is missing/nonpositive"))
        else:
            seen.add(ticker)
            usable.append({**peer, "ticker": ticker, "pe": peer["price"] / peer["diluted_eps"]})
    return usable, rejected


def median(numbers):
    ordered = sorted(numbers)
    midpoint = len(ordered) // 2
    return ordered[midpoint] if len(ordered) % 2 else (ordered[midpoint - 1] + ordered[midpoint]) / 2


def implied_prices(usable, target_data):
    if not valid_positive_number(target_data["diluted_eps"]) or not usable:
        return None
    multiples = [peer["pe"] for peer in usable]
    target_eps = target_data["diluted_eps"]
    return {"minimum": min(multiples) * target_eps, "median": median(multiples) * target_eps, "maximum": max(multiples) * target_eps}


def main():
    usable, rejected = usable_peers(target, peers)
    print("Peer P/E multiples")
    for peer in usable:
        print(f"{peer['ticker']}: {peer['pe']:.6f}x")
    for ticker, reason in rejected:
        print(f"{ticker}: {reason}")

    results = implied_prices(usable, target)
    if results is None:
        print("\nNo usable peers: no implied price estimate.")
        return
    if len(usable) == 1:
        print(f"\nOne valid peer: reference estimate ${results['median']:.2f}; no range.")
    else:
        print(f"\nPeer median P/E: {median([peer['pe'] for peer in usable]):.6f}x")
        print(f"Implied price range: ${results['minimum']:.2f}–${results['maximum']:.2f}")
        print(f"Implied price at peer median: ${results['median']:.2f}")

    full_median_price = results["median"]
    print("\nLeave-one-peer-out results")
    for removed_peer in usable:
        remaining = [peer for peer in usable if peer["ticker"] != removed_peer["ticker"]]
        remaining_results = implied_prices(remaining, target)
        if remaining_results is None:
            print(f"Remove {removed_peer['ticker']}: no estimate (no peers remain).")
        else:
            price = remaining_results["median"]
            label = "reference estimate" if len(remaining) == 1 else "median-implied price"
            print(f"Remove {removed_peer['ticker']}: {label} ${price:.2f}; change ${price - full_median_price:+.2f}")


if __name__ == "__main__":
    main()
