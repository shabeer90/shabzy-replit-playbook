// A call that writes somewhere else (email, storage, payments, webhooks) has only succeeded if its
// result says so (PLAYBOOK rule 20). Wrap the awaited result:
//   checked(await resend.emails.send(msg), "contact email")
// Throws on false, null, undefined or a result with an `error`; returns the result otherwise.
// scripts/check_external_writes.py fails CI when a known write isn't wrapped.
export function checked<T>(result: T, what: string): Exclude<T, false | null | undefined> {
  if (result === false || result === null || result === undefined) {
    throw new Error(`${what} failed: no result`);
  }
  const error = (result as { error?: unknown }).error;
  if (error) {
    throw new Error(`${what} failed: ${error instanceof Error ? error.message : JSON.stringify(error)}`);
  }
  return result as Exclude<T, false | null | undefined>;
}
