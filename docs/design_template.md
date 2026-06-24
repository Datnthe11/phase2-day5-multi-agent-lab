# Design Template

## Problem

Hệ thống cần nhận một câu truy vấn nghiên cứu phức tạp (ví dụ: "Research GraphRAG state-of-the-art"), tự động tìm kiếm thông tin mới nhất trên mạng, phân tích trích xuất các ý chính yếu và quan điểm khác nhau, sau đó tổng hợp thành một báo cáo hoàn chỉnh có trích dẫn nguồn rõ ràng.

## Why multi-agent?

Single-agent gặp khó khăn khi phải đồng thời đóng nhiều vai trò: vừa tìm kiếm, vừa phân tích và vừa viết lách trong một context window giới hạn, rất dễ bị "ảo giác" (hallucinate) hoặc bỏ sót ý. Bằng cách tách thành Multi-agent, mỗi Agent (Researcher, Analyst, Writer) có một System Prompt chuyên biệt giúp tăng độ chính xác, giảm nhầm lẫn và dễ dàng scale hoặc debug từng khâu.

## Agent roles

| Agent | Responsibility | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Điều hướng luồng chạy của hệ thống giữa các Agent | ResearchState hiện tại | Route tiếp theo (Researcher/Analyst/Writer/FINISH) | Lặp vòng lặp vô tận nếu routing sai |
| Researcher | Tìm kiếm thông tin trên Web và tóm tắt nguồn | `request.query`, `max_sources` | `sources`, `research_notes` | Không tìm thấy kết quả từ Search API |
| Analyst | Phân tích notes, trích xuất ý chính và quan điểm | `research_notes` | `analysis_notes` | Trích xuất sai lệch nội dung |
| Writer | Viết báo cáo tổng hợp cuối cùng có trích dẫn | `research_notes`, `analysis_notes` | `final_answer` | Báo cáo bị cụt do giới hạn output tokens |

## Shared state

- `request` (ResearchQuery): Chứa câu hỏi gốc và cấu hình tìm kiếm. Cần để định hướng cho các Agent.
- `sources` (List[SourceDocument]): Chứa các URL và snippet đã tìm được. Cần để Writer trích dẫn.
- `research_notes` (str): Ghi chú thu thập được từ Researcher.
- `analysis_notes` (str): Các phân tích từ Analyst.
- `final_answer` (str): Câu trả lời cuối cùng.
- `route_history` (List[str]): Lịch sử định tuyến để Supervisor tránh lặp vòng lặp vô hạn.
- `agent_results` (List[AgentResult]): Lưu trữ lịch sử hành động và token tiêu thụ của từng Agent.

## Routing policy

```text
       [START]
          |
          v
   +--------------+
   |  Supervisor  | <------------------------------------+
   +--------------+                                      |
          |                                              |
          |---(if 'researcher' not in route_history)---> Researcher
          |                                              |
          |---(if 'analyst' not in route_history)------> Analyst
          |                                              |
          |---(if 'writer' not in route_history)-------> Writer
          |
          v
       [FINISH]
```

## Guardrails

- Max iterations: 6 (Được cấu hình trong Config)
- Timeout: 60s (Giới hạn trong Config)
- Retry: Có thể thêm Langchain Retry parser nếu LLM output sai schema.
- Fallback: Trả về thông báo lỗi nếu Search API bị sập.
- Validation: Dùng Pydantic `AgentResult` với chuỗi `Enum` nghiêm ngặt để đảm bảo tên Agent chuẩn.

## Benchmark plan

- **Query**: "Research GraphRAG state-of-the-art"
- **Metric**: Latency (thời gian chạy), Estimated Cost USD (tính từ token), Quality Score (1-10 chấm tự động bởi LLM).
- **Expected outcome**: Multi-agent mất nhiều thời gian hơn, tốn chi phí hơn Single-agent nhưng bù lại điểm Quality cao vượt trội nhờ có facts và citations chuẩn xác.
