import Foundation

let helper = URLSessionHelper.shared
let session = URLSession(configuration: .ephemeral)
defer { session.invalidateAndCancel() }
let url = URL(string: "https://example.invalid/response")!
let first = session.dataTask(with: url)
let second = session.dataTask(with: url)
let chunks = (0..<128).map { Data(repeating: UInt8($0), count: 65536) }
var expected = Data()
let started = Date()
for chunk in chunks {
    helper.setOrAppend(chunk, for: first)
    helper.setOrAppend(Data([42]), for: second)
    expected.append(chunk)
}
precondition(helper.obtainData(for: first) == expected, "chunk order or payload corrupted")
precondition(helper.obtainData(for: first) == nil, "completed body delivered twice")
precondition(helper.obtainData(for: second) == Data(repeating: 42, count: chunks.count), "same-URL tasks collided")
helper.setOrAppend(Data([1, 2, 3]), for: first)
helper.discardData(for: first)
precondition(helper.obtainData(for: first) == nil, "discard retained response body")
print("PASS: real response buffer, interleaved tasks, 8 MiB body, single delivery and discard (\(Date().timeIntervalSince(started))s)")
