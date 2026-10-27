import { redirect } from "next/navigation";

export default function MockPage({
  searchParams,
}: {
  searchParams: { id?: string; paper_id?: string; exam_id?: string };
}) {
  const paperId = searchParams.id || searchParams.paper_id || searchParams.exam_id || "2026-06-set1";
  redirect(`/full-paper?id=${paperId}`);
}
