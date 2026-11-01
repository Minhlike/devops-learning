"""Compile designed learning units; this never awards learning credit."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SESSIONS = [
('Docker','Image bất biến và container là lần chạy','PID 1 và vòng đời process'),
('Docker','Writable layer và volume','DNS dịch vụ và port publishing'),
('Docker','Health không phải restart policy','CPU quota, memory và graceful shutdown'),
('Docker','Build context, cache và multi-stage','Registry digest và artifact promotion'),
('GitHub','Job cô lập và cổng test ba codebase','Chuyển cùng artifact giữa jobs'),
('GitHub','Quyền workflow và pull request không tin cậy','Required checks và dependency gate'),
('GitHub','Environment approval và quyền deploy','Rollback binary và tương thích schema'),
('GitHub','Dependency và secret scanning','Release record và provenance'),
('AWS','Principal, role và explicit deny','STS session và kiểm danh tính'),
('AWS','Subnet, route và đường phản hồi','EC2 bootstrap và ranh giới Security Group'),
('AWS','S3 object khác EBS block','Snapshot, backup và restore thử'),
('AWS','RDS connection và pool của Java','Transaction boundary và migration'),
('AWS','Load balancer và target readiness','Autoscaling khác database capacity'),
('AWS','DNS cache và TTL khi đổi dịch vụ','TLS termination và đường tới upstream'),
('AWS','Metric, log và retention có giá','Alarm có owner và giới hạn chi phí'),
('Terraform','Configuration, state và hạ tầng thật','Provider graph và partial apply'),
('Terraform','Reference suy diễn dependency','Network module và output contract'),
('Terraform','Remote backend, lock và backup state','Module interface và scope quyền'),
('Terraform','Resource address và for_each','Import, moved và replacement có dữ liệu'),
('Ansible','Inventory, connection và module','Idempotency và trạng thái changed'),
('Ansible','Role interface và variable scope','Handler notification và restart có điều kiện'),
('Ansible','Inventory groups và giới hạn blast radius','Serial deployment và partial failure'),
('Ansible','Vault encryption và quyền giải mã','Tags, check mode và bằng chứng hội tụ'),
('Kubernetes','API, etcd và reconciliation','Kubelet, scheduler và container runtime'),
('Kubernetes','Service selector và EndpointSlice','CNI, DNS và NetworkPolicy'),
('Kubernetes','ConfigMap và vòng đời cấu hình','Startup, readiness và liveness'),
('Kubernetes','Request, limit và scheduling','CPU utilization, metrics và HPA'),
('Kubernetes','PVC, PV và storage ownership','Stateful workload và restore dữ liệu'),
('Kubernetes','Gateway listener, route và backend','Kind LoadBalancer và giới hạn môi trường'),
('Helm','Chart template và values contract','Upgrade, diff và rollback có điều kiện'),
('Kubernetes','Điều tra Pending, pull và probe','Recovery có stop rule và hậu điều kiện'),
('Prometheus','Counter, rate và reset','Scrape target và cardinality'),
('Grafana','Query, unit và cửa sổ dashboard','Phân biệt No Data với dữ liệu bằng không'),
('Logging','Request ID qua Java và worker','Log pipeline, retention và dữ liệu nhạy cảm'),
('Prometheus','Pending, firing và alert evaluation','Routing, silence và kiểm kênh thông báo'),
]
SOURCES = {
'Docker':('https://docs.docker.com/engine/containers/run/','Running containers','Engine API/CLI; verify installed version'),
'GitHub':('https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax','Jobs, needs, permissions','GitHub Actions rolling docs'),
'AWS':('https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html','Pillars and design principles','AWS service/Region must be checked before lab'),
'Terraform':('https://developer.hashicorp.com/terraform/language','State, resources, expressions','Terraform version pinned by future lab lock'),
'Ansible':('https://docs.ansible.com/ansible-core/2.19/','Playbooks, handlers, check mode','ansible-core 2.19 design target'),
'Kubernetes':('https://kubernetes.io/docs/concepts/','Workloads, networking, storage','Design target v1.35; verify APIs on actual cluster'),
'Helm':('https://helm.sh/docs/','Charts and releases','Verify Helm major before authored lab'),
'Prometheus':('https://prometheus.io/docs/prometheus/latest/querying/basics/','Expression language data types','Version selected at lab authoring'),
'Grafana':('https://grafana.com/docs/grafana/latest/panels-visualizations/','Panels and visualizations','Version selected at lab authoring'),
'Logging':('https://opentelemetry.io/docs/concepts/signals/logs/','Log correlation','OpenTelemetry concepts; backend selected later'),
}

def main():
    lessons=[]
    previous=None
    for session, (tech,*titles) in enumerate(SESSIONS,14):
        for index,title in enumerate(titles,1):
            lid=f'R-S{session:02d}-C{index:02d}'
            url,section,version=SOURCES[tech]
            row=dict(id=lid,legacy_session=f'S{session}',title=title,technology=tech,
                     prerequisites=[previous] if previous else [],maturity='DESIGNED',
                     content=None,guided_lab=None,independent_lab=None,
                     competency=f'Giải thích và kiểm chứng {title.lower()} trong OrderOps',
                     evidence_required=['concept','guided','independent'],operational_required=False,
                     official_docs=[dict(url=url,section=section,version=version,
                        purpose='Đọc cơ chế, đối chiếu hành vi và giới hạn theo phiên bản')],
                     levels=['Foundation','Applied','Troubleshooting','Advanced Extension'],
                     certification=dict(status='NOT_MAPPED',reason='Chưa kiểm exam blueprint; không suy readiness thi từ lesson'))
            if session==14:
                row.update(maturity='AUTHORED',content=f'docs/relearning/lessons/{lid}.md',
                           guided_lab=f'relearning-labs/{lid}/GUIDED.md',
                           independent_lab=f'relearning-labs/{lid}/INDEPENDENT.md')
                if index==2:
                    row['official_docs']=[dict(url='https://docs.docker.com/reference/cli/docker/container/stop/',section='Stop container: signal and timeout',version='Docker Engine Linux; check installed version',purpose='Distinguish graceful termination and forced kill'),dict(url='https://docs.docker.com/reference/builder/#entrypoint',section='ENTRYPOINT exec and shell form',version='Dockerfile reference rolling, checked 2026-11-01',purpose='Trace signal delivery to the main process')]
            lessons.append(row); previous=lid
    p=ROOT/'docs/relearning/catalog.json'; p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(dict(schema_version=1,track='relearning',lessons=lessons),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Curriculum S14–S48','', '70 đơn vị kiến thức; AUTHORED chỉ nói nội dung đã viết, không trao mastery cho học viên.','',
           '| Buổi | Lesson | Mô hình tư duy | Nội dung |','|---|---|---|---|']
    for x in lessons: lines.append(f"| {x['legacy_session']} | {x['id']} | {x['title']} | {x['maturity']} |")
    (p.parent/'CURRICULUM.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__': main()
