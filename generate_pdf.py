import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
from reportlab.lib.units import cm

def build_pdf():
    pdf_filename = "/mnt/d/Devops/LINUX_DEVOPS_CHEATSHEET.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=1.2*cm,
        leftMargin=1.2*cm,
        topMargin=1.2*cm,
        bottomMargin=1.2*cm
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=12
    )

    h2_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#38bdf8")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    table_body_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title & Header
    story.append(Paragraph("BO CHEAT SHEET LINUX &amp; DEVOPS COT LOI", title_style))
    story.append(Paragraph("DevOps Personal Tutor System | Path: D:\\Devops", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#2563eb"), spaceAfter=10))

    # Section 1: Grammar & Anatomy
    story.append(Paragraph("1. CAU TRUC NGU PHAP CU PHAP LINUX (COMMAND LINE ANATOMY)", h2_style))
    grammar_text = (
        "<b>Cong thuc chung:</b> Command [-Options/Flags] [Arguments]<br/>"
        "• <b>Command:</b> File chuong trinh thuc thi (/bin, /usr/bin).<br/>"
        "• <b>- (Co ngan 1 ky tu):</b> ls -la, rm -rf (Co the gop nhieu co).<br/>"
        "• <b>-- (Co dai tu day du):</b> --help, --version, --no-pager.<br/>"
        "• <b>&gt; (Ghi de):</b> Xoa sach va ghi moi. | <b>&gt;&gt; (Ghi noi):</b> Ghi them vao cuoi file.<br/>"
        "• <b>| (Pipe):</b> Dau noi dau ra (stdout) cua lenh trai lam dau vao (stdin) cho lenh phai."
    )
    story.append(Paragraph(grammar_text, body_style))
    story.append(Spacer(1, 8))

    # Section 2: Filesystem Hierarchy
    story.append(Paragraph("2. CAY HE THONG FILE LINUX (FILESYSTEM HIERARCHY)", h2_style))
    fs_data = [
        [Paragraph("Thu muc", table_header_style), Paragraph("Khai niem &amp; Vai tro cot loi", table_header_style)],
        [Paragraph("<b>/</b>", table_body_style), Paragraph("<b>Root Directory:</b> Thu muc goc toi cao cua he thong Linux.", table_body_style)],
        [Paragraph("<b>/home</b>", table_body_style), Paragraph("Thu muc ca nhan cua nguoi dung (vi du /home/minh123).", table_body_style)],
        [Paragraph("<b>/etc</b>", table_body_style), Paragraph("Noi chua toan bo <b>FILE CAU HINH</b> cua HDH va phan mem (Nginx, SSH...).", table_body_style)],
        [Paragraph("<b>/var</b>", table_body_style), Paragraph("Noi chua <b>DU LIEU BIEN DOI</b> (Log /var/log, cache, database).", table_body_style)],
        [Paragraph("<b>/proc</b>", table_body_style), Paragraph("Thu muc ao chua thong tin phan cung CPU/RAM &amp; Process tu RAM.", table_body_style)],
        [Paragraph("<b>/tmp</b>", table_body_style), Paragraph("Thu muc chua file tam thoi (tu dong xoa khi reboot).", table_body_style)],
        [Paragraph("<b>/mnt/d</b>", table_body_style), Paragraph("Noi WSL2 mount o dia D: cua Windows vao Linux.", table_body_style)]
    ]
    t_fs = Table(fs_data, colWidths=[2.5*cm, 15*cm])
    t_fs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_fs)
    story.append(Spacer(1, 8))

    # Section 3: Core File Operations
    story.append(Paragraph("3. THAO TAC FILE &amp; THU MUC CO BAN", h2_style))
    file_ops_code = (
        "pwd                                  # In duong dan thu muc hien tai\n"
        "cd /duong/dan                        # Di chuyen thu muc (cd .. lui 1 cap, cd ~ ve home)\n"
        "ls -la                               # In chi tiet tat ca file/folder ke ca file an .\n"
        "mkdir -p folder1/folder2             # Tao chuoi thu muc long nhau cùng luc\n"
        "touch filename.txt                   # Tao file rong moi\n"
        "cp -r nguon dich                     # Sao chep file/folder (-r cho folder)\n"
        "mv nguon dich                        # Di chuyen HOAC doi ten file/folder\n"
        "rm -rf folder_name                   # Xoa de quy folder/file ep buoc khong hoi\n"
        "cat filename                         # In toan bo noi dung file ra man hinh\n"
        "head -n 10 filename                  # Xem 10 dong dau tien cua file\n"
        "tail -n 20 filename                  # Xem 20 dong cuoi cung cua file\n"
        "grep \"tu_khoa\" filename              # Loc tim kiem dong chua tu khoa"
    )
    p_ops = Paragraph(file_ops_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
    t_ops = Table([[p_ops]], colWidths=[17.5*cm])
    t_ops.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ops)
    story.append(Spacer(1, 8))

    # Section 4: Permissions
    story.append(Paragraph("4. PHAN QUYEN &amp; QUAN LY USER (chmod, chown, sudo)", h2_style))
    perm_intro = "<b>Bang diem Octal:</b> Read (r=4), Write (w=2), Execute (x=1). Doi tuong: User (u) | Group (g) | Others (o)."
    story.append(Paragraph(perm_intro, body_style))
    story.append(Spacer(1, 4))

    perm_data = [
        [Paragraph("Ma so", table_header_style), Paragraph("Chuoi chu", table_header_style), Paragraph("Y nghia &amp; Truong hop su dung", table_header_style)],
        [Paragraph("<b>755</b>", table_body_style), Paragraph("rwxr-xr-x", table_body_style), Paragraph("Mac dinh cho Thu muc &amp; Script thuc thi (Owner toan quyen, Group/Others chi doc/chay).", table_body_style)],
        [Paragraph("<b>644</b>", table_body_style), Paragraph("rw-r--r--", table_body_style), Paragraph("Mac dinh cho File du lieu thuong (Owner doc/ghi, Group/Others chi doc).", table_body_style)],
        [Paragraph("<b>600</b>", table_body_style), Paragraph("rw-------", table_body_style), Paragraph("Bat buoc cho <b>SSH Private Key</b> (Chi Owner doc/ghi, cam tuyet doi nguoi khac).", table_body_style)]
    ]
    t_perm = Table(perm_data, colWidths=[2*cm, 3*cm, 12.5*cm])
    t_perm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_perm)
    story.append(Spacer(1, 4))

    perm_code = (
        "chmod +x script.sh                   # Cap quyen thuc thi cho file script\n"
        "chmod 600 ~/.ssh/id_ed25519          # Phan quyen chuan bao mat cho SSH Private Key\n"
        "sudo chown root:root filename        # Doi nguoi so huu file sang user root"
    )
    p_perm_c = Paragraph(perm_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
    t_perm_c = Table([[p_perm_c]], colWidths=[17.5*cm])
    t_perm_c.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_perm_c)
    story.append(Spacer(1, 8))

    # Section 5: Process & Services
    story.append(Paragraph("5. QUAN LY TIEN TRINH &amp; DICH VU (PROCESS &amp; SYSTEMD)", h2_style))
    ps_code = (
        "ps aux | grep ten_tien_trinh          # Tim PID (Process ID) cua tien trinh dang chay\n"
        "kill -9 <PID>                        # Ep buoc dung ngay lap tuc tien trinh bi treo\n"
        "top / htop                           # Man hinh giam sat CPU/RAM realtime\n"
        "sudo systemctl status nginx          # Xem trang thai dich vu Nginx\n"
        "sudo systemctl start|stop|restart nginx # Khoi chay / Dung / Khoi dong lai dich vu\n"
        "sudo systemctl enable nginx          # Cho phep dich vu tu bat khi khoi dong may\n"
        "sudo journalctl -u nginx -n 50 --no-pager # Xem 50 dong log moi nhat cua Nginx\n"
        "sudo nginx -t                        # Kiem tra cu phap file cau hinh Nginx"
    )
    p_ps = Paragraph(ps_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
    t_ps = Table([[p_ps]], colWidths=[17.5*cm])
    t_ps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ps)
    story.append(Spacer(1, 8))

    # Section 6: APT & Recovery
    story.append(Paragraph("6. QUAN LY GOI &amp; SUA SU CO (APT &amp; INCIDENT RECOVERY)", h2_style))
    apt_code = (
        "sudo apt update && sudo apt install -y package_name # Cap nhat danh sach &amp; cai dat goi\n"
        "sudo apt purge -y package_name                      # Xoa sach goi + XOA TOAN BO CONFIG IN /etc/\n"
        "curl -I http://localhost                            # Kiem tra Header phan hoi HTTP Server"
    )
    p_apt = Paragraph(apt_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
    t_apt = Table([[p_apt]], colWidths=[17.5*cm])
    t_apt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_apt)
    story.append(Spacer(1, 8))

    # Section 7: Git for DevOps
    story.append(Paragraph("7. GIT &amp; GITHUB CO BAN DANH CHO DEVOPS", h2_style))
    git_code = (
        "ssh-keygen -t ed25519 -C \"email@example.com\" # Sinh SSH Key chuan Ed25519\n"
        "ssh -T git@github.com                        # Kiem tra ket noi SSH toi GitHub\n"
        "git init                                     # Khoi tao kho Git local\n"
        "git branch -M main                           # Doi ten nhanh mac dinh thanh main\n"
        "git status                                   # Kiem tra trang thai lam viec\n"
        "git add .                                    # Dua tat ca file vao Staging Area\n"
        "git commit -m \"feat: mo ta cong viec\"        # Chup anh luu tru commit\n"
        "git remote add origin git@github.com:User/Repo.git # Ket noi remote GitHub\n"
        "git remote -v                                # Kiem tra duong dan Remote hien co\n"
        "git remote rename origion origin             # Sua loi go nham ten Remote\n"
        "git push -u origin main                      # Day commit len nhanh main tren GitHub"
    )
    p_git = Paragraph(git_code.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
    t_git = Table([[p_git]], colWidths=[17.5*cm])
    t_git.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0f172a")),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_git)

    doc.build(story)
    print("PDF build successful:", pdf_filename)

if __name__ == '__main__':
    build_pdf()
