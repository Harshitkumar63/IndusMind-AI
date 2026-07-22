"use client";

import {
  CircleDot,
} from "lucide-react";
import { useState, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  type Node,
  type Edge,
  type NodeTypes,
  Handle,
  Position,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

/* ═══════════════════════════════════════════════════════════
   Node Colors by Type
   ═══════════════════════════════════════════════════════════ */

const NODE_COLORS: Record<string, { bg: string; border: string; text: string }> = {
  equipment: { bg: "rgba(99,102,241,0.15)", border: "#6366f1", text: "#a5b4fc" },
  person: { bg: "rgba(34,197,94,0.15)", border: "#22c55e", text: "#86efac" },
  department: { bg: "rgba(139,92,246,0.15)", border: "#8b5cf6", text: "#c4b5fd" },
  location: { bg: "rgba(6,182,212,0.15)", border: "#06b6d4", text: "#67e8f9" },
  sop: { bg: "rgba(245,158,11,0.15)", border: "#f59e0b", text: "#fcd34d" },
  regulation: { bg: "rgba(239,68,68,0.15)", border: "#ef4444", text: "#fca5a5" },
  incident: { bg: "rgba(244,63,94,0.15)", border: "#f43f5e", text: "#fda4af" },
  process: { bg: "rgba(16,185,129,0.15)", border: "#10b981", text: "#6ee7b7" },
  material: { bg: "rgba(107,114,128,0.15)", border: "#6b7280", text: "#d1d5db" },
};

/* ═══════════════════════════════════════════════════════════
   Custom Node Component
   ═══════════════════════════════════════════════════════════ */

function CustomNode({ data }: { data: { label: string; nodeType: string; properties?: Record<string, string> } }) {
  const colors = NODE_COLORS[data.nodeType] || NODE_COLORS.material;
  return (
    <div
      className="px-4 py-3 rounded-xl shadow-lg min-w-[140px] max-w-[200px] cursor-pointer transition-all hover:scale-105"
      style={{
        background: colors.bg,
        border: `1.5px solid ${colors.border}`,
        backdropFilter: "blur(8px)",
      }}
    >
      <Handle type="target" position={Position.Top} className="!w-2 !h-2 !border-0" style={{ background: colors.border }} />
      <Handle type="source" position={Position.Bottom} className="!w-2 !h-2 !border-0" style={{ background: colors.border }} />
      <div className="flex items-center gap-2 mb-1">
        <CircleDot className="w-3 h-3 shrink-0" style={{ color: colors.border }} />
        <span className="text-[10px] uppercase tracking-wider font-medium" style={{ color: colors.border }}>
          {data.nodeType}
        </span>
      </div>
      <p className="text-sm font-semibold leading-snug" style={{ color: colors.text }}>
        {data.label}
      </p>
      {data.properties?.role && (
        <p className="text-[10px] mt-1 opacity-60" style={{ color: colors.text }}>{data.properties.role}</p>
      )}
    </div>
  );
}

const nodeTypes: NodeTypes = { custom: CustomNode };

/* ═══════════════════════════════════════════════════════════
   Graph Data
   ═══════════════════════════════════════════════════════════ */

const GRAPH_NODES: Record<string, { type: string; name: string; properties?: Record<string, string> }> = {
  n1: { type: "equipment", name: "Pump P-101", properties: { type: "centrifugal" } },
  n2: { type: "equipment", name: "Compressor C-201" },
  n3: { type: "equipment", name: "HX E-301" },
  n4: { type: "equipment", name: "Boiler B-401" },
  n5: { type: "department", name: "Mechanical Eng." },
  n6: { type: "department", name: "Process Eng." },
  n7: { type: "department", name: "Safety Dept." },
  n8: { type: "person", name: "Rajesh Kumar", properties: { role: "Sr. Maintenance Eng." } },
  n9: { type: "person", name: "Priya Sharma", properties: { role: "Safety Officer" } },
  n10: { type: "person", name: "Amit Patel", properties: { role: "Plant Manager" } },
  n11: { type: "location", name: "Unit-1 Process" },
  n12: { type: "location", name: "Unit-2 Utilities" },
  n13: { type: "sop", name: "SOP-M-001" },
  n14: { type: "sop", name: "SOP-S-003" },
  n15: { type: "regulation", name: "OSHA PSM" },
  n16: { type: "regulation", name: "ISO 10816-3" },
  n17: { type: "incident", name: "INC-042: Seal Leak" },
  n18: { type: "incident", name: "INC-038: Tube Fail" },
  n19: { type: "process", name: "Cooling Water Sys." },
  n20: { type: "material", name: "316 Stainless Steel" },
};

const GRAPH_EDGES_DATA = [
  { source: "n1", target: "n5", label: "maintained_by" },
  { source: "n1", target: "n8", label: "maintained_by" },
  { source: "n1", target: "n11", label: "located_in" },
  { source: "n1", target: "n13", label: "governed_by" },
  { source: "n1", target: "n17", label: "related_to" },
  { source: "n1", target: "n16", label: "governed_by" },
  { source: "n2", target: "n5", label: "maintained_by" },
  { source: "n2", target: "n11", label: "located_in" },
  { source: "n3", target: "n6", label: "maintained_by" },
  { source: "n3", target: "n12", label: "located_in" },
  { source: "n3", target: "n18", label: "related_to" },
  { source: "n3", target: "n19", label: "part_of" },
  { source: "n3", target: "n20", label: "uses" },
  { source: "n4", target: "n12", label: "located_in" },
  { source: "n4", target: "n15", label: "governed_by" },
  { source: "n9", target: "n7", label: "part_of" },
  { source: "n10", target: "n6", label: "part_of" },
  { source: "n14", target: "n7", label: "governed_by" },
  { source: "n17", target: "n8", label: "inspected_by" },
  { source: "n18", target: "n6", label: "inspected_by" },
];

/* ═══════════════════════════════════════════════════════════
   Layout Generation
   ═══════════════════════════════════════════════════════════ */

function generateLayout() {
  const nodes: Node[] = [];
  const typeGroups: Record<string, string[]> = {};

  Object.entries(GRAPH_NODES).forEach(([id, node]) => {
    if (!typeGroups[node.type]) typeGroups[node.type] = [];
    typeGroups[node.type].push(id);
  });

  const typeOrder = ["equipment", "department", "person", "location", "sop", "regulation", "incident", "process", "material"];
  let y = 0;

  typeOrder.forEach((type) => {
    const ids = typeGroups[type] || [];
    const totalWidth = ids.length * 220;
    const startX = -totalWidth / 2 + 110;

    ids.forEach((id, i) => {
      const node = GRAPH_NODES[id];
      nodes.push({
        id,
        type: "custom",
        position: { x: startX + i * 220, y },
        data: { label: node.name, nodeType: node.type, properties: node.properties },
      });
    });

    if (ids.length > 0) y += 160;
  });

  const edges: Edge[] = GRAPH_EDGES_DATA.map((e, i) => ({
    id: `e-${i}`,
    source: e.source,
    target: e.target,
    label: e.label,
    type: "smoothstep",
    animated: true,
    style: { stroke: "rgba(99,102,241,0.3)", strokeWidth: 1.5 },
    labelStyle: { fill: "var(--muted-foreground)", fontSize: 9 },
    labelBgStyle: { fill: "var(--card)", fillOpacity: 0.9 },
  }));

  return { nodes, edges };
}

/* ═══════════════════════════════════════════════════════════
   Knowledge Graph Page
   ═══════════════════════════════════════════════════════════ */

export default function KnowledgeGraphPage() {
  const { nodes: initNodes, edges: initEdges } = useMemo(() => generateLayout(), []);
  const [nodes, , onNodesChange] = useNodesState(initNodes);
  const [edges, , onEdgesChange] = useEdgesState(initEdges);
  const [selectedType, setSelectedType] = useState<string | null>(null);

  const nodeTypeList = Object.keys(NODE_COLORS);

  return (
    <div className="space-y-4 -m-6">
      {/* Header */}
      <div className="px-6 pt-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Knowledge Graph</h1>
          <p className="text-[var(--muted-foreground)] text-sm mt-1">
            Interactive visualization of entity relationships extracted from documents
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="badge badge-primary">{Object.keys(GRAPH_NODES).length} Nodes</span>
          <span className="badge badge-info">{GRAPH_EDGES_DATA.length} Edges</span>
        </div>
      </div>

      {/* Legend */}
      <div className="px-6 flex flex-wrap items-center gap-2">
        {nodeTypeList.map((type) => {
          const colors = NODE_COLORS[type];
          const isActive = selectedType === null || selectedType === type;
          return (
            <button
              key={type}
              onClick={() => setSelectedType(selectedType === type ? null : type)}
              className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium capitalize transition-all ${
                isActive ? "opacity-100" : "opacity-40"
              }`}
              style={{
                background: colors.bg,
                borderColor: colors.border,
                color: colors.text,
                border: `1px solid ${colors.border}`,
              }}
            >
              <CircleDot className="w-3 h-3" />
              {type.replace("_", " ")}
            </button>
          );
        })}
      </div>

      {/* Graph */}
      <div className="h-[calc(100vh-250px)] border-t border-[var(--border)]">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          minZoom={0.3}
          maxZoom={2}
          proOptions={{ hideAttribution: true }}
          style={{ background: "var(--background)" }}
        >
          <Background color="var(--border)" gap={30} size={1} />
          <Controls
            showInteractive={false}
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: "10px",
            }}
          />
          <MiniMap
            nodeColor={(node) => {
              const type = (node.data as { nodeType?: string })?.nodeType || "material";
              return NODE_COLORS[type]?.border || "#6b7280";
            }}
            maskColor="rgba(0,0,0,0.6)"
            style={{
              background: "var(--card)",
              border: "1px solid var(--border)",
              borderRadius: "10px",
            }}
          />
        </ReactFlow>
      </div>
    </div>
  );
}
