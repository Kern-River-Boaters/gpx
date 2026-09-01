---
name: "mac-compute-node"
description: "mac-compute-node skill for OpenCode"
---

# mac-compute-node

> Parent Skill Definition: [mac-compute-node](file:///home/jpino/Obsidian/Genealogy/_Meta/Skills/mac-compute-node/SKILL.md)

---
name: mac-compute-node
description: "Operational skill and procedural runbook for leveraging the pino-family-imac Apple Silicon / Mac node as a dedicated distributed compute accelerator (Apple Vision Neural Engine OCR, CoreML, Metal GPU acceleration, PDF rasterization, and multi-threaded document ingestion over Tailscale/SSH) across federated Obsidian vaults under ADR-020, ADR-GEN-022, and SYS-INF-016."
---

# 🍏 Mac Compute Node & Apple Vision Accelerator Standard

Governed under **SYS-INF-016 (Distributed Workstation Compute Mesh)**, **ADR-020 (Archival Vision Engine)**, and **ADR-GEN-022 (Hermes Document Extraction Ontology & Level 4 Provenance)**.

---

## 🎯 1. Overview & Architecture

The `pino-family-imac` node provides high-throughput hardware-accelerated offloading from the primary Linux workstation (`kern`):
* **Apple Vision Framework (`VNRecognizeTextRequest`)**: Ultra-high accuracy, hardware-accelerated OCR running on the Apple Neural Engine (ANE) and GPU/CPU with native multi-lingual support (English, Spanish, French, Latin).
* **Throughput SLA**: Sub-100ms per high-resolution document image; 10–20 pages/second over multi-threaded SSH worker pools.
* **Zero External Dependencies**: Uses native Swift compilation against system frameworks (`Vision`, `AppKit`, `CoreImage`).

```
                    KERN (Linux Master Workstation)
                                   │
                   ┌───────────────┴───────────────┐
                   ▼                               ▼
         Digital Vector Text             Raster Images & Scans
         (Parallel pdftotext)            (Streaming Worker Pool)
                                                   │
                                                   ▼ SSH Stream
                                     PINO-FAMILY-IMAC (Mac Node)
                                     ┌─────────────────────────┐
                                     │ /tmp/apple_vision_ocr   │
                                     │ • Apple Vision Neural   │
                                     │ • Multi-threaded Swift  │
                                     │ • Bilingual (ES/EN)     │
                                     └─────────────────────────┘
                                                   │
                                                   ▼ JSON / Text Stream
                                     HERMES KINSHIP PARSER
                                     (Updates Vault Companion Notes)
```

---

## 🛠️ 2. Apple Vision Swift OCR Binary (`apple_vision_ocr`)

The Mac node hosts a compiled, optimized Mach-O binary `/tmp/apple_vision_ocr` built with `swiftc -O`:

```swift
import Foundation
import Vision
import AppKit

guard CommandLine.arguments.count > 1 else {
    print("Usage: apple_vision_ocr <image-path-or-stdin>")
    exit(1)
}

let imagePath = CommandLine.arguments[1]
let url = URL(fileURLWithPath: imagePath)

guard let image = NSImage(contentsOf: url),
      let tiffData = image.tiffRepresentation,
      let ciImage = CIImage(data: tiffData) else {
    fputs("Error: Unable to load image at \(imagePath)\n", stderr)
    exit(1)
}

let request = VNRecognizeTextRequest { (request, error) in
    guard let observations = request.results as? [VNRecognizedTextObservation] else { return }
    let text = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
    print(text)
}

request.recognitionLevel = .accurate
request.recognitionLanguages = ["en-US", "es-ES", "fr-FR"]
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(ciImage: ciImage, options: [:])
try? handler.perform([request])
```

---

## 🚀 3. Multi-Worker Invocation Standard

When executing batch extraction from Python scripts on `kern`:
1. **Parallel Thread Pool**: Use `concurrent.futures.ThreadPoolExecutor(max_workers=12)`.
2. **SSH Connection Pooling / Multiplexing**: Reuse persistent ControlMaster connections to `pino-family-imac` to eliminate SSH handshake overhead:
   ```bash
   ssh -o ControlMaster=auto -o ControlPath=/tmp/ssh-mac-%r@%h:%p -o ControlPersist=10m pino-family-imac
   ```
3. **Payload Streaming**: Stream image bytes via stdin or staged temp buffers to avoid unnecessary disk I/O.

---

## 🛡️ 4. Operational Invariants

1. **Host Safeguards**: Do not block Lisa's interactive desktop usage; limit worker threads to $\le 16$ to maintain UI responsiveness on the Mac.
2. **Git-Crypt Safety**: Because binary decryption is handled authoritatively on `kern`, always stream decrypted assets directly from `kern`'s verified CAS storage (`.blobs/` / `Sources/`).
3. **Fallback Grace Period**: If the Mac is offline or sleeping, gracefully fall back to local `pdftotext` and CPU extraction on `kern` without failing the pipeline.

