from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    """
    비밀번호 재설정 토큰 생성을 위한 클래스
    Args:
        PasswordResetTokenGenerator (class)
    """

    def _make_hash_value(self, user, timestamp):
        """
        토근 생성에 사용되는 해시 값 생성하는 메서드
        Args:
            user (User): 유저 객체
            timestamp (int): timestamp

        Returns:
            _type_: str
        """
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()