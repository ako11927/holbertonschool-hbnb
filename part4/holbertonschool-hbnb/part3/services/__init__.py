"""Services package"""
try:
    from .facade_final import facade_final as facade
    print("Using final facade")
except ImportError as e:
    print(f"Warning: Could not import final facade: {e}")
    try:
        from .facade_simple import facade_simple as facade
        print("Using simple facade")
    except ImportError:
        try:
            from .facade import facade
            print("Using main facade")
        except ImportError:
            print("Warning: Could not import any facade")
            facade = None
