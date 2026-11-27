// JSON-LD goes into <script> via dangerouslySetInnerHTML, where a `</script>` inside any string value
// (scraped or model-written) would end the block. JSON allows \u003c for `<`, so the data is unchanged.
// Usage: <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: toJsonLd(data) }} />
export const toJsonLd = (value: unknown): string => JSON.stringify(value).replace(/</g, '\\u003c')
