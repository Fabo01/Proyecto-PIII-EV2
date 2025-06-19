class Map:
    def __init__(self):
        self._data = {}

    def __getitem__(self, k):
        """Return the value associated with key k, else raise KeyError."""
        if k not in self._data:
            raise KeyError(f"Key {k} not found")
        return self._data[k]

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting if existing."""
        self._data[k] = v

    def __delitem__(self, k):
        """Remove item with key k, else raise KeyError."""
        if k not in self._data:
            raise KeyError(f"Key {k} not found")
        del self._data[k]

    def __len__(self):
        """Return number of items in the map."""
        return len(self._data)

    def __iter__(self):
        """Iterate over keys in the map."""
        return iter(self._data)

    def __contains__(self, k):
        """Return True if key k exists in the map."""
        return k in self._data

    def get(self, k, d=None):
        """Return M[k] if exists, else return default d."""
        return self._data.get(k, d)

    def setdefault(self, k, d=None):
        """Return M[k] if exists, else set M[k]=d and return d."""
        return self._data.setdefault(k, d)

    def pop(self, k, d=None):
        """Remove and return item with key k, else return d (or raise KeyError if d=None)."""
        if d is None:
            return self._data.pop(k)  # Raises KeyError if k missing
        return self._data.pop(k, d)

    def popitem(self):
        """Remove and return arbitrary (k,v) pair. Raise KeyError if empty."""
        return self._data.popitem()

    def clear(self):
        """Remove all items from the map."""
        self._data.clear()

    def keys(self):
        """Return a view of all keys."""
        return self._data.keys()

    def values(self):
        """Return a view of all values."""
        return self._data.values()

    def items(self):
        """Return a view of all (k,v) pairs."""
        return self._data.items()

    def update(self, M2):
        """Update map with key/value pairs from M2, overwriting existing keys."""
        self._data.update(M2)

    def __eq__(self, M2):
        """Return True if M and M2 have identical key-value pairs."""
        if not isinstance(M2, Map):
            return False
        return self._data == M2._data

    def __ne__(self, M2):
        """Return True if M and M2 differ in any key-value pair."""
        return not (self == M2)

    def __str__(self):
        """String representation of the map."""
        return str(self._data)
    


m = Map()
m["name"] = "Alice"  # __setitem__
print(m["name"])      # __getitem__ → "Alice"
print(len(m))         # __len__ → 1
print("name" in m)    # __contains__ → True

m.update({"age": 30}) # update
print(m.items())      # items() → dict_items([('name', 'Alice'), ('age', 30)])

m2 = Map()
m2.update(m)
print(m == m2)        # __eq__ → True