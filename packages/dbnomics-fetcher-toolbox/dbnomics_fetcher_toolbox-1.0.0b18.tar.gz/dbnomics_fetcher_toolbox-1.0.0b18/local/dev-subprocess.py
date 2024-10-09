# ruff: noqa: F401, INP001, T201, UP006, UP035
# %%

import subprocess

from iterable_subprocess import iterable_subprocess

# %%

with iterable_subprocess(
    ["/usr/bin/xmlindent", "-i", "2"],
    [b"<x></m>"],
) as output:
    for chunk in output:
        print(chunk)

# %%

process = subprocess.Popen(
    ["/usr/bin/xmlindent", "-i", "2"],  # noqa: S603
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

# %%

process.wait()

# %%

process.stdin.write(b"<x")

# %%

process.stdin.flush()

# %%

process.stdin.close()

# %%

process.stdout.read(1)

# %%

process.stdout.close()


# %%

process.communicate()

# %%

with subprocess.Popen(
    ["/usr/bin/xmlindent", "-i", "2"],  # noqa: S603
    stdin=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdout=subprocess.PIPE,
) as process:
    process.stdin.write(b"<x")
    print(iter(process.stdout.read(), b""), flush=True)
    stdout_data, stderr_data = process.communicate(b"<x>")
    # print((stdout_data, stderr_data), flush=True)
    # stdout_data, stderr_data = process.communicate(b"</x>")
    # print((stdout_data, stderr_data), flush=True)

    process.stdin.close()
