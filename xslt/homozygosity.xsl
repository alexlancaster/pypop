<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

 <!-- ################  HOMOZYGOSITY STATISTICS ###################### --> 
 
 <xsl:template match="homozygosity">
  <xsl:call-template name="section">
   <xsl:with-param name="title">
    <xsl:call-template name="locus-header">
     <xsl:with-param name="title">
      <xsl:text>Ewens-Watterson homozygosity test of neutrality</xsl:text>
     </xsl:with-param>
    </xsl:call-template>
   </xsl:with-param>
   <xsl:with-param name="level" select="3"/>
   <xsl:with-param name="text">

    <xsl:choose>

     <xsl:when test="@role='out-of-range'">
      <xsl:text>*Out of range of simulated homozygosity values*</xsl:text>
      <xsl:call-template name="newline"/>
      <xsl:text>*can't estimate expected homozygosity*</xsl:text>
     </xsl:when>
     
     <xsl:otherwise>
      
      <!-- print specified fields then do templates for pvalue -->

      <xsl:text>Observed F: </xsl:text>
      <xsl:value-of select="observed"/>
      <xsl:text>, Expected F: </xsl:text>
      <xsl:value-of select="expected"/>
      <xsl:text>, Normalized deviate (Fnd): </xsl:text>
      <xsl:value-of select="normdev"/>
      <xsl:call-template name="newline"/>
      <xsl:text>p-value range: </xsl:text>

      <!-- treat pvalue differently, since it is not a simple value, but
      has an upper and lower bound -->
      <xsl:apply-templates select="pvalue" mode="bounded"/>
     </xsl:otherwise>
    </xsl:choose>
   </xsl:with-param>
  </xsl:call-template>
 </xsl:template>

 <!-- get significance for two-tailed test -->
 <xsl:template name="get-significance-two-tailed">
  <xsl:param name="lower"/>
  <xsl:param name="upper"/>

   <!-- 
   a two tailed test implies testing both end of distribution:

   5%:    0.005 < p <= 0.025 OR 0.975 <= p < 0.995        (*)
   1%:    0.0005 < p <= 0.005 OR 0.995 <= p < 0.9995      (**)
   0.1%:  0.00005 < p <= 0.0005 OR 0.9995 <= p < 0.99995  (***)
   0.01%: p <= 0.00005 OR p >= 0.99995                    (****)
   -->

  <xsl:choose>

  <xsl:when test="($upper &lt;= 0.00005) or ($lower &gt;= 0.99995)">4</xsl:when>
   <xsl:when test="($upper &lt;= 0.0005) or ($lower &gt;= 0.9995)">3</xsl:when>

   <xsl:when test="($upper &lt;= 0.005) or ($lower &gt;= 0.995)">2</xsl:when>

   <xsl:when test="($upper &lt;= 0.025) or ($lower &gt;= 0.975)">1</xsl:when>

<!-- more strict test, that assumes we have an exact value, rather 
     a than range

  <xsl:when test="($upper &lt;= 0.00005)
    or ($lower &gt;= 0.99995)">4</xsl:when>

   <xsl:when test="($upper &lt;= 0.0005 and $lower &gt; 0.00005)
    or ($upper &lt;= 0.99995 and $lower &gt; 0.9995)">3</xsl:when>
   <xsl:when test="($upper &lt;= 0.005 and $lower &gt; 0.0005)
    or ($upper &lt;= 0.9995 and $lower &gt; 0.995)">2</xsl:when>

   <xsl:when test="($upper &lt;= 0.025 and $lower &gt; 0.005)
    or ($upper &lt;= 0.995 and $lower &gt; 0.975)">1</xsl:when>
-->
 
   <xsl:otherwise>0</xsl:otherwise>
  </xsl:choose>
 </xsl:template>
 
 <xsl:template match="pvalue" mode="bounded">
  
  <xsl:value-of select="lower"/><xsl:text disable-output-escaping="yes"> &lt; p &lt;= </xsl:text><xsl:value-of select="upper"/>
  <xsl:text> </xsl:text> 

  <xsl:call-template name="append-pad">
   <xsl:with-param name="padChar">*</xsl:with-param>
   <xsl:with-param name="length">
    <xsl:call-template name="get-significance-two-tailed">
     <xsl:with-param name="lower" select="lower"/>
     <xsl:with-param name="upper" select="upper"/>
    </xsl:call-template>
   </xsl:with-param>
  </xsl:call-template>

  </xsl:template>

 <!-- ################  END HOMOZYGOSITY STATISTICS ###################### --> 

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
 