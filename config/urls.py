from graphene_django.views import GraphQLView

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path(
        "graphql",
        csrf_exempt(GraphQLView.as_view(graphiql=settings.DEBUG)),
        name="graphql",
    )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
