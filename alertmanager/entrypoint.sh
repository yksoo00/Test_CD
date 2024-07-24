#!/bin/sh

# 환경변수를 템플릿 파일에 주입하여 실제 설정 파일을 생성
sed "s|\${API_URL}|${API_URL}|g" /etc/alertmanager/alertmanager.yml.tmpl > /etc/alertmanager/alertmanager.yml

# Alertmanager 실행
/bin/alertmanager "$@"