<xsl:stylesheet 
 version='1.0'
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 xmlns:exsl="http://exslt.org/common"
 extension-element-prefixes="exsl"
 xmlns:data="any-uri">

 <xsl:import href="lib.xsl"/>

 <!-- select "text" as output method -->
 <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

 <data:map-order>
  <locusname order="1">A</locusname>
  <locusname order="2">C</locusname>
  <locusname order="3">B</locusname>
  <locusname order="4">DRA</locusname>
  <locusname order="5">DRB1</locusname>
  <locusname order="6">DQA1</locusname>
  <locusname order="7">DQB1</locusname>
  <locusname order="8">DPA1</locusname>
  <locusname order="9">DPB1</locusname>
 </data:map-order>

 <data:region-order>
  <regionname long="Sub-Saharan-Africa">1.Sub-Sah-Africa</regionname>
  <regionname long="North-African">2.N-Africa</regionname>	  
  <regionname long="Europe">3.Europe</regionname>	  
  <regionname long="South-West-Asia">4.SW-Asia</regionname>	  
  <regionname long="South-East-Asia">5.SE-Asia</regionname>	  
  <regionname long="Oceania">6.Oceania</regionname>	  
  <regionname long="North-East-Asia">7.NE-Asia</regionname>	  
  <regionname long="North-America">8.N-America</regionname>	  
  <regionname long="South-America">9.S-America</regionname>	  
  <regionname long="Other">10.Other</regionname>          
 </data:region-order>

 <xsl:param name="map-order" 
  select="document('')//data:map-order/locusname"/>

 <xsl:param name="region-order" 
  select="document('')//data:region-order/regionname"/>

 <xsl:variable name="all-allele-list" select="document('allelelist-by-locus.xml', .)/allelelist-by-locus"/>

 <!-- suppress output of random text -->
 <xsl:template match="text()"/>

 <xsl:template name="phylip-lines">
  <xsl:param name="nodes"/>

  <xsl:text>     </xsl:text>
  <xsl:value-of select="count($nodes)"/>
  <xsl:text> </xsl:text>
  <xsl:value-of select="count($all-allele-list/locus[.!=''])"/>
  <xsl:call-template name="newline"/>

  <xsl:for-each select="$all-allele-list/locus">
   <xsl:if test="count(allele)!=0">
    <xsl:value-of select="count(allele)"/>
    <xsl:text> </xsl:text>
   </xsl:if>
  </xsl:for-each>

  <xsl:call-template name="newline"/>

  <xsl:for-each select="$nodes">

   <xsl:call-template name="append-pad">
    <xsl:with-param name="padVar">
     <xsl:value-of select="populationdata/popname"/>
    </xsl:with-param>
    <xsl:with-param name="length" select="9"/>
   </xsl:call-template>
   <xsl:text> </xsl:text>
   
   <xsl:for-each select="locus">
    <xsl:variable name="curlocus" select="@name"/>
    <xsl:variable name="cur-allele-list" select="allelecounts/allele"/>
    
    <xsl:for-each select="$all-allele-list/locus[@name=$curlocus]/allele">
     <xsl:variable name="allelename" select="."/>
     <xsl:choose>
      <xsl:when test="$cur-allele-list[@name=$allelename]">
       <xsl:value-of select="normalize-space($cur-allele-list[@name=$allelename]/frequency)"/>
      </xsl:when>
      <xsl:otherwise>0.00000</xsl:otherwise>
     </xsl:choose>
     <xsl:text> </xsl:text>
    </xsl:for-each>
   </xsl:for-each>
   <xsl:call-template name="newline"/>
  </xsl:for-each>
 
</xsl:template>
 
 <xsl:template name="line-start">
  <xsl:param name="popnode"/>
  
  <xsl:value-of select="translate($popnode/popname, ' ', '-')"/>
  <xsl:text>&#09;</xsl:text>
  <xsl:value-of select="translate($popnode/ethnic, ' ', '-')"/>
  <xsl:text>&#09;</xsl:text>
  <!-- apply short form of regions as defined in lookup table -->
  <xsl:value-of select="$region-order[@long=translate($popnode/contin, ' ', '-')]"/>
  <xsl:text>&#09;</xsl:text>
 </xsl:template>

 <xsl:template name="gen-lines">
  <xsl:param name="nodes"/>
  <xsl:param name="type" select="'1'"/>

  <xsl:for-each select="$nodes">

   <xsl:choose>
    <xsl:when test="$type='1-locus-summary'">

     <xsl:call-template name="line-start">
      <xsl:with-param name="popnode" select="../populationdata"/>
     </xsl:call-template>

     <xsl:value-of select="translate(@name, '*', '')"/>
     <xsl:text>&#09;</xsl:text>

     <xsl:choose>
      <xsl:when test="allelecounts/allelecount">
       <xsl:value-of select="allelecounts/allelecount"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>

     <xsl:text>&#09;</xsl:text>

     <xsl:choose>
      <xsl:when test="allelecounts/distinctalleles">
       <xsl:value-of select="allelecounts/distinctalleles"/>
      </xsl:when>
      <xsl:otherwise>0</xsl:otherwise>
     </xsl:choose>

     <xsl:text>&#09;</xsl:text>
     <xsl:choose>
      <xsl:when test="homozygosity=''">
       <xsl:text>****&#09;****&#09;****</xsl:text>
      </xsl:when>
      <xsl:otherwise>
       <xsl:value-of select="homozygosity/pvalue/lower"/>
       <xsl:text>&#09;</xsl:text>
       <xsl:value-of select="homozygosity/pvalue/upper"/>
       <xsl:text>&#09;</xsl:text>
       <xsl:value-of select="homozygosity/normdev"/>
      </xsl:otherwise>
     </xsl:choose>
     <xsl:text>&#09;</xsl:text>
     <xsl:choose>
      <xsl:when test="hardyweinbergGuoThompson=''">
       <xsl:text>****</xsl:text>
      </xsl:when>
      <xsl:otherwise>
       <xsl:value-of select="hardyweinbergGuoThompson/pvalue"/>
      </xsl:otherwise>
     </xsl:choose>
     
     <xsl:text>&#09;</xsl:text>
     <xsl:choose>
      <!--complete -->
      <xsl:when
       test="hardyweinberg/lumped/@role='no-rare-genotypes' and 
       hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <!-- common + lumped -->
      <xsl:when test="hardyweinberg/lumped!='' and 
       hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <!-- common -->
      <xsl:when test="hardyweinberg/common!=''">
       <xsl:value-of select="hardyweinberg/common/pvalue"/>
      </xsl:when>
      <xsl:otherwise>****</xsl:otherwise>
     </xsl:choose>

     <xsl:text>&#09;</xsl:text>
     <xsl:choose>
      <xsl:when test="hardyweinberg/homozygotes/pvalue">
       <xsl:value-of select="hardyweinberg/homozygotes/pvalue"/>
      </xsl:when>
      <xsl:otherwise>****</xsl:otherwise>
     </xsl:choose>

     <xsl:text>&#09;</xsl:text>
     <xsl:choose>
      <xsl:when test="hardyweinberg/heterozygotes/pvalue">
       <xsl:value-of select="hardyweinberg/heterozygotes/pvalue"/>
      </xsl:when>
      <xsl:otherwise>****</xsl:otherwise>
     </xsl:choose>

     <xsl:call-template name="newline"/>

    </xsl:when>

    <xsl:when test="$type='2-locus-summary'">

     <xsl:call-template name="line-start">
      <xsl:with-param name="popnode" select="../../populationdata"/>
     </xsl:call-template>
     
     <xsl:value-of
     select="number(individcount[@role='after-filtering']) * 2"/>
     <xsl:text>&#09;</xsl:text>

     <xsl:variable name="locus1" select="substring-before(@loci, ':')"/>
     <xsl:variable name="locus2" select="substring-after(@loci, ':')"/>

     <!-- make sure locus1 and locus2 are always in map order -->
     <xsl:choose>
      <xsl:when test="$map-order[.=$locus1]/@order &lt;
       $map-order[.=$locus2]/@order">
       <xsl:value-of select="$locus1"/>
       <xsl:text>&#09;</xsl:text>
       <xsl:value-of select="$locus2"/>
      </xsl:when>
      <xsl:otherwise>
       <xsl:value-of select="$locus2"/>
       <xsl:text>&#09;</xsl:text>
       <xsl:value-of select="$locus1"/>
      </xsl:otherwise>
     </xsl:choose>

     <xsl:text>&#09;</xsl:text>
     <xsl:value-of select="linkagediseq/summary/dprime"/>
     <xsl:text>&#09;</xsl:text>
     <xsl:value-of select="linkagediseq/summary/wn"/>
     <xsl:text>&#09;</xsl:text>
     <xsl:value-of select="linkagediseq/summary/q/chisq"/>
     <xsl:text>&#09;</xsl:text>
     <xsl:value-of select="linkagediseq/summary/q/dof"/>
     <xsl:call-template name="newline"/>
     
    </xsl:when>


    <xsl:when test="$type='2-locus-haplo'">

     <xsl:variable name="curr-line-start">
      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../../populationdata"/>
      </xsl:call-template>

      <xsl:value-of select="substring-before(@loci,':')"/>
      <xsl:text>:</xsl:text>
      <xsl:value-of select="substring-after(@loci, ':')"/>
     </xsl:variable>

     <xsl:for-each select="haplotypefreq/haplotype">
      <xsl:value-of select="$curr-line-start"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="@name"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="frequency"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="numCopies"/>
      <xsl:text>&#09;</xsl:text>

      <xsl:variable name="first">
       <xsl:value-of select="substring-before(@name, ':')"/>
       <xsl:text>:</xsl:text>
      </xsl:variable>
      <xsl:variable name="second">
       <xsl:value-of select="substring-after(@name, ':')"/>
      </xsl:variable>

      <xsl:variable name="pair"
      select="../../linkagediseq/loci[1]/allelepair[@first=$first and
      @second=$second]"/>

      <xsl:value-of select="$pair/norm_dij"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="$pair/chisq"/>

      <xsl:call-template name="newline"/>

     </xsl:for-each>
    </xsl:when>

    <xsl:when test="$type='1-locus-allele'">

     <xsl:variable name="curr-line-start">
      <xsl:call-template name="line-start">
       <xsl:with-param name="popnode" select="../populationdata"/>
      </xsl:call-template>
     </xsl:variable>

     <xsl:for-each select="allelecounts/allele">
      <xsl:value-of select="$curr-line-start"/>

      <xsl:value-of select="../../@name"/>
      <xsl:text>&#09;</xsl:text>

      <xsl:value-of select="@name"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="frequency"/>
      <xsl:text>&#09;</xsl:text>
      <xsl:value-of select="count"/>
      <xsl:call-template name="newline"/>
     </xsl:for-each>
    </xsl:when>
   </xsl:choose>
   
   
  </xsl:for-each>
 </xsl:template>

 <xsl:template match="/">


  <xsl:choose>

   <xsl:when test="element-available('exsl:document')">

    <exsl:document href="1-locus-summary.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:text>pop&#09;ethnic&#09;region&#09;locus&#09;2n&#09;k&#09;f.pval.lower&#09;f.pval.upper&#09;f.nd&#09;gt.pval&#09;hw.chisq.pval&#09;hw.homo.chisq.pval&#09;hw.het.chisq.pval</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
      <xsl:with-param name="type" select="'1-locus-summary'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="1-locus-allele.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:text>pop&#09;ethnic&#09;region&#09;locus&#09;allele&#09;allele.freq&#09;allele.count</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis/locus"/>
      <xsl:with-param name="type" select="'1-locus-allele'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="2-locus-summary.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:text>pop&#09;ethnic&#09;region&#09;n.haplo&#09;locus1&#09;locus2&#09;ld.dprime&#09;ld.wn&#09;q.chisq&#09;q.df</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis/emhaplofreq/group[@mode='haplo' and (string-length(@loci) - string-length(translate(@loci, ':', '')))=1]"/>
      <xsl:with-param name="type" select="'2-locus-summary'"/>
     </xsl:call-template>
    </exsl:document>

    <exsl:document href="2-locus-haplo.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:text>pop&#09;ethnic&#09;region&#09;locus&#09;allele&#09;allele.freq&#09;allele.count&#09;ld.dprime&#09;ld.chisq</xsl:text>
     <xsl:call-template name="newline"/>
     <xsl:call-template name="gen-lines">
      <xsl:with-param name="nodes"
      select="/meta/dataanalysis/emhaplofreq/group[@mode='haplo' and (string-length(@loci) - string-length(translate(@loci, ':', '')))=1]"/>
      <xsl:with-param name="type" select="'2-locus-haplo'"/>
     </xsl:call-template>
    </exsl:document>


    <exsl:document href="phylip.dat"
     omit-xml-declaration="yes"
     method="text">
     <xsl:call-template name="phylip-lines">
      <xsl:with-param name="nodes" select="/meta/dataanalysis"/>
     </xsl:call-template>
    
    </exsl:document>


    </xsl:when>

   <xsl:otherwise>
    <xsl:message>needs a processor that understands exsl elements, see http://exsl.org/
    </xsl:message>
   </xsl:otherwise>
  </xsl:choose>

 </xsl:template>

</xsl:stylesheet>

<!-- 
Local variables:
mode: xml
sgml-default-dtd-file: "xsl.ced"
sgml-indent-step: 1
sgml-indent-data: 1
End:
-->
