# Create your views here.

from ine.models import dict_ccaa, dict_provinces, dict_municipalities
from ine.serializers import dict_ccaa_Serializer, dict_provinces_Serializer, dict_municipalities_Serializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from scripts.utils import normalize_text


class dict_ccaa_List(APIView):
    """
    Retrieve a list with all CCAA.
    """

    def get(self, request):
        ccaa = dict_ccaa.objects.all()
        serializer = dict_ccaa_Serializer(ccaa, many=True)
        return Response(serializer.data)


class ccaa_Detail(APIView):

    def get_object(self, nombre):
        try:
            return dict_ccaa.objects.get(NOMBRE=nombre)
        except dict_ccaa.DoesNotExist:
            raise Http404

    def get(self, request, nombre):
        """
        Retrieve a list with the NOMBRE of a CA.
        <br>
        ####    * Required NOMBRE.
        ####    Example: Andalucía
        """
        ccaa = self.get_object(nombre)
        serializer = dict_ccaa_Serializer(ccaa)
        return Response(serializer.data)


class dict_provinces_List(APIView):
    """
    Retrieve a list with all CCAA.
    """

    def get(self, request):
        provinces = dict_provinces.objects.all()
        serializer = dict_provinces_Serializer(provinces, many=True)
        return Response(serializer.data)


class provinces_Detail(APIView):

    def get_object(self, nombre):
        try:
            return dict_provinces.objects.get(NOMBRE=nombre)
        except dict_provinces.DoesNotExist:
            raise Http404

    def get(self, request, nombre):
        """
        Retrieve a list with the NOMBRE of a province.
        <br>
        ####    * Required NOMBRE.
        ####    Example: Cádiz
        """
        provinces = self.get_object(nombre)
        serializer = dict_provinces_Serializer(provinces)
        return Response(serializer.data)


class dict_municipalities_List(APIView):
    """
    Retrieve a list with all CCAA.
    """

    def get(self, request):
        municipalities = dict_municipalities.objects.all()
        serializer = dict_municipalities_Serializer(municipalities, many=True)
        return Response(serializer.data)


class municipalities_Detail(APIView):

    def get_object(self, nombre):
        try:
            return dict_municipalities.objects.get(NOMBRE=nombre)
        except dict_municipalities.DoesNotExist:
            raise Http404

    def get(self, request, nombre):
        """
        Retrieve a list with the NOMBRE of a municipalitie.
        <br>
        ####    * Required NOMBRE.
        ####    Example: Jerez de la Frontera
        """
        municipalities = self.get_object(nombre)
        serializer = dict_municipalities_Serializer(municipalities)
        return Response(serializer.data)


class suggest_Nombre(APIView):
    """
    Retrieve a list with suggested names for an input string.
    <br>
    ####    * Required NOMBRE.
    ####    Example: jerez
    """

    def get(self, request, nombre):
        ccaa = dict_ccaa.objects.values_list('NOMBRE', flat=True)
        provinces = dict_provinces.objects.values_list('NOMBRE', flat=True)
        municipalities = dict_municipalities.objects.values_list('NOMBRE', flat=True)

        results = []
        for c in ccaa:
            result = normalize_text.evaluate_strings(nombre, c)
            if result:
                result['source'] = 'Comunidad Autónoma'
                results.append(result)

        for p in provinces:
            result = normalize_text.evaluate_strings(nombre, p)
            if result:
                result['source'] = 'Provincia'
                results.append(result)

        for m in municipalities:
            result = normalize_text.evaluate_strings(nombre, m)
            if result:
                result['source'] = 'Municipio'
                results.append(result)

        results = sorted(results, key=lambda d: d['score_%'], reverse=True)

        nombres = []
        for r in results:
            nombres.append({"Nombre": r['string'], "Entidad": r['source']})

        return Response(nombres)
