
from metrics import TransferMetrics

metrics = TransferMetrics()

metrics.record_packet(512)
metrics.record_packet(512)
metrics.record_packet(512, retransmission=True)

metrics.report()