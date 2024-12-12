import datetime
import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from DIVA.models import DichVu, BaiViet
from DIVA.forms import DichVuForm, BaiVietForm
from docx import Document
from django.conf import settings
import os

def is_staff_or_admin(user):
    return user.is_staff or user.is_superuser

def is_admin(user):
    return user.is_superuser

def ve_chung_toi(request):
    return render (request,'dich_vu/ve_chung_toi.html')

@user_passes_test(is_staff_or_admin)
def danh_sach_dich_vu(request):
    tu_khoa = request.GET.get('q', '')
    if tu_khoa:
        dich_vu_list = DichVu.objects.filter(ten__icontains=tu_khoa)
    else:
        dich_vu_list = DichVu.objects.all()
    return render(request, 'dich_vu/danh_sach.html', {'dich_vu_list': dich_vu_list, 'tu_khoa': tu_khoa})

@user_passes_test(is_staff_or_admin)
def them_dich_vu(request):
    if request.method == 'POST':
        form = DichVuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_dich_vu')
    else:
        form = DichVuForm()
    return render(request, 'dich_vu/them_dich_vu.html', {'form': form})

@user_passes_test(is_staff_or_admin)
def cap_nhat_dich_vu(request, MaDV):
    dich_vu = get_object_or_404(DichVu, MaDV=MaDV)

    if request.method == 'POST':
        form = DichVuForm(request.POST, instance=dich_vu)
        if form.is_valid():
            form.save()
            # Thêm thông báo cập nhật thành công
            messages.success(request, f"Dịch vụ '{dich_vu.ten}' đã được cập nhật thành công!")
            return redirect('danh_sach_dich_vu')  # Redirect về danh sách dịch vụ sau khi lưu
    else:
        form = DichVuForm(instance=dich_vu)

    return render(request, 'dich_vu/cap_nhat_dich_vu.html', {'form': form, 'dich_vu': dich_vu})

@user_passes_test(is_staff_or_admin)
def xoa_dich_vu(request, MaDV):
    dich_vu = get_object_or_404(DichVu, MaDV=MaDV)
    if request.method == 'POST':
        dich_vu.delete()
        return redirect('danh_sach_dich_vu')
    return render(request, 'dich_vu/xoa_dich_vu.html', {'dich_vu': dich_vu})

@user_passes_test(is_staff_or_admin)
def tao_bai_viet(request):
    if request.method == 'POST':
        form = BaiVietForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('danh_sach_bai_viet')  # Điều hướng tới danh sách bài viết
    else:
        form = BaiVietForm()
    return render(request, 'dich_vu/tao_bai_viet.html', {'form': form})


def danh_sach_bai_viet(request):
    query = request.GET.get('q', '')  # Lấy giá trị từ trường tìm kiếm 'q', mặc định là chuỗi rỗng
    if query:
        bai_viet_list = BaiViet.objects.filter(tieu_de__icontains=query).order_by('-ngay_tao')
    else:
        bai_viet_list = BaiViet.objects.order_by('-ngay_tao')

    return render(request, 'dich_vu/danh_sach_bai_viet.html', {'bai_viet_list': bai_viet_list, 'query': query})


def process_docx(file_path):
    """
    Đọc file .docx và chuyển nội dung sang HTML, giữ nguyên thứ tự văn bản và ảnh, thêm định dạng cho chữ.
    """
    doc = Document(file_path)
    html_content = ""
    fs = FileSystemStorage()
    media_folder = settings.MEDIA_ROOT
    image_counter = 1  # Đặt tên cho ảnh duy nhất

    # Duyệt qua từng phần tử trong document
    for block in doc.element.body.iter():
        if block.tag.endswith("p"):  # Đoạn văn
            text_content = "".join(node.text for node in block.iter() if node.tag.endswith("t") and node.text)

            # Kiểm tra nếu đoạn văn là heading
            if block.tag.endswith("p") and hasattr(block, "pPr"):  # Kiểm tra style
                style_node = block.find(".//w:pStyle", namespaces=doc.part.element.nsmap)
                if style_node is not None and style_node.attrib.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val", "").startswith("Heading"):
                    html_content += f"<h2 style='font-weight: bold; color: #c08c19; font-size: 30px; text-align: left;'>{text_content}</h2>"
                else:
                    paragraph_html = "<p style='font-size: 16px;'>"
                    for node in block.iter():
                        if node.tag.endswith("t") and node.text:
                            text = node.text

                            # Xử lý định dạng danh sách
                            if ":" in text:
                                before_colon, after_colon = text.split(":", 1)
                                paragraph_html += f"<span style='font-weight: bold;'>{before_colon}:</span>{after_colon}"
                            else:
                                paragraph_html += text

                    paragraph_html += "</p>"
                    html_content += paragraph_html

        elif block.tag.endswith("r"):  # Hình ảnh trong đoạn văn
            for child in block.iter():
                if child.tag.endswith("blip"):  # Tìm thẻ <blip> chứa ảnh
                    image_data = doc.part.related_parts[child.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"]].blob
                    image_name = f"docx_image_{image_counter}.png"
                    image_counter += 1
                    image_path = os.path.join(media_folder, image_name)

                    # Lưu hình ảnh vào thư mục media
                    if not os.path.exists(image_path):
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_data)

                    # Chèn ảnh vào HTML tại vị trí hiện tại
                    image_url = fs.url(image_name)
                    html_content += f'<div class="image-container"><img src="{image_url}" alt="Image"></div>'

    return html_content

def chi_tiet_bai_viet(request, bai_viet_id):
    bai_viet = get_object_or_404(BaiViet, id=bai_viet_id)
    file_content = None

    if bai_viet.noi_dung and bai_viet.noi_dung.path.endswith('.docx'):
        file_path = bai_viet.noi_dung.path
        file_content = process_docx(file_path)

    return render(request, 'dich_vu/chi_tiet_bai_viet.html', {
        'bai_viet': bai_viet,
        'file_content': file_content,
    })