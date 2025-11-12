from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


def validate_gender(gender_list):
    if all(g in ['남', '여'] for g in gender_list):
        return None
    else:
        return "성별 입력 오류: '남' 또는 '여'만 입력 가능합니다."

def format_languages(lang_list):
    return ", ".join(lang_list)


@app.route('/')
def main_page():
    empty_data = {
        'team_name': "",
        'leader_name': "",
        'leader_gender': "",
        'leader_role': "",
        'leader_department': "",
        'leader_language': "",
        'leader_email': "",
        'leader_photo': "",
        'members': [] # 팀원 리스트는 빈 리스트로 전달
    }
    return render_template('input.html', **empty_data)
                           
@app.route('/result', methods=['POST'])
def process_team_data():
    # 1. 팀명 추출
    team_name = request.form['team_name']

    # 2. 팀장 정보 추출
    leader_data = {
        'leader_name': request.form['leader_name'],
        'leader_gender': request.form['leader_gender'],
        'leader_role': request.form['leader_role'],
        'leader_department': request.form['leader_department'],
        'leader_language': request.form['leader_language'],
        'leader_email': request.form['leader_email'],
        'leader_photo': request.form.get('leader_photo', 'images/leader.jpg')
    }

    # 3. 팀원 정보 추출 (리스트)
    member_names = request.form.getlist('member_name[]')
    member_genders = request.form.getlist('member_gender[]')
    member_roles = request.form.getlist('member_role[]')
    member_departments = request.form.getlist('member_department[]')
    member_languages = request.form.getlist('member_language[]')
    member_emails = request.form.getlist('member_email[]')
    member_photos = request.form.getlist('member_photo[]')

    # 4. 팀원 모듈 함수 호출 및 검증
    gender_error = validate_gender(member_genders)
    
    # 5. 팀원 데이터 통합
    members_data = []
    member_data_list = zip(member_names, member_genders, member_roles, member_departments, member_languages, member_emails, member_photos)
    
    for name, gender, role, dept, lang, email, photo in member_data_list:
        members_data.append({
            'name': name,
            'gender': gender,
            'role': role,
            'department': dept,
            'language': lang,
            'email': email,
            'photo': photo if photo else 'images/member.jpg'
        })
    
    # 6. 결과 페이지 렌더링에 사용할 최종 데이터
    output_data = {
        'team_name': team_name,
        'members': members_data,
        'language_summary': format_languages(member_languages),
        'error': gender_error,
        **leader_data
    }
    
    return render_template('result.html', **output_data)

if __name__ == '__main__':
    app.run(debug=True)