from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# 서버가 유지되는 동안 저장되는 팀 데이터
team_data = {
    "team_name": "HelloWorld",
    "leader": {
        "name": "송민교",
        "role": "팀장",
        "department": "정보통신공학과",
        "gender": "여",
        "language": "Swift",
        "email": "2023111948@dgu.ac.kr",
        "phone": "010-0000-1111",
        "photo": "images/leader.jpg"
    },
    "members": [
        {
            "name": "추상윤",
            "role": "팀원",
            "department": "정보통신공학과",
            "gender": "남",
            "language": "Java",
            "email": "2023111949@dgu.ac.kr",
            "phone": "010-0000-2222",
            "photo": "images/member1.jpg"
        },
        {
            "name": "김동찬",
            "role": "팀원",
            "department": "정보통신공학과",
            "gender": "남",
            "language": "Java",
            "email": "2021111349@dgu.ac.kr",
            "phone": "010-0000-3333",
            "photo": "images/member2.jpg"
        },
        {
            "name": "이승희",
            "role": "팀원",
            "department": "화학과",
            "gender": "남",
            "language": "Java",
            "email": "lsh2222@dgu.ac.kr",
            "phone": "010-0000-2222",
            "photo": "images/member3.jpg"
        }
    ]
}

# 메인 페이지
@app.route('/')
def index():
    return render_template(
        'app_index.html',
        team_name=team_data["team_name"],
        leader=team_data["leader"],
        members=team_data["members"]
    )

# 팀 정보 입력 (기존 정보 자동 표시)
@app.route('/input')
def input():
    return render_template(
        'app_input.html',
        team_name=team_data["team_name"],
        leader=team_data["leader"],
        members=team_data["members"]
    )

# 팀 정보 제출 후 결과 반영
@app.route('/result', methods=['POST'])
def result():
    global team_data

    team_name = request.form.get('team_name')

    leader = {
        'name': request.form.get('leader_name'),
        'role': request.form.get('leader_role'),
        'gender': request.form.get('leader_gender'),
        'department': request.form.get('leader_department'),
        'language': request.form.get('leader_language'),
        'email': request.form.get('leader_email'),
        'phone': request.form.get('leader_phone', ''), 
        'photo': request.form.get('leader_photo') or 'images/leader.jpg'
    }

    members = []
    names = request.form.getlist('member_name[]')
    genders = request.form.getlist('member_gender[]')
    roles = request.form.getlist('member_role[]')
    departments = request.form.getlist('member_department[]')
    languages = request.form.getlist('member_language[]')
    emails = request.form.getlist('member_email[]')
    photos = request.form.getlist('member_photo[]')

    for i in range(len(names)):
        members.append({
            'name': names[i],
            'gender': genders[i],
            'role': roles[i],
            'department': departments[i],
            'language': languages[i],
            'email': emails[i],
            'phone': '',
            'photo': photos[i] if photos[i] else 'images/member1.jpg'
        })

    # 저장
    team_data["team_name"] = team_name
    team_data["leader"] = leader
    team_data["members"] = members

    return redirect(url_for('index'))  # 결과 후 메인으로 이동

# 팀 연락처 입력 페이지
@app.route('/contact')
def contact():
    return render_template(
        'app_contact.html',
        leader=team_data["leader"],
        members=team_data["members"]
    )

# 연락처 저장
@app.route('/contact_save', methods=['POST'])
def contact_save():
    global team_data

    team_data["leader"]["phone"] = request.form.get('leader_phone')
    team_data["leader"]["email"] = request.form.get('leader_email')

    member_phones = request.form.getlist('member_phone[]')
    member_emails = request.form.getlist('member_email[]')

    for i, m in enumerate(team_data["members"]):
        if i < len(member_phones):
            m["phone"] = member_phones[i]
        if i < len(member_emails):
            m["email"] = member_emails[i]

    return redirect(url_for('index'))  # 저장 후 메인 페이지로 이동


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
